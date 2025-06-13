#!/usr/bin/env python3
"""
Document Watcher Service
Monitors Nextcloud shared folder for new PDF/DOCX files
and automatically imports them to Paperless NGX.
"""

import os
import time
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from loguru import logger
from fastapi import FastAPI
import uvicorn
import threading

# Configuration
WATCH_FOLDER = os.getenv('WATCH_FOLDER', '/shared')
PAPERLESS_CONSUME_FOLDER = os.getenv('PAPERLESS_CONSUME_FOLDER', '/paperless-consume')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Supported file extensions
SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.doc'}

# Setup logging
logger.add("/app/logs/watcher.log", rotation="10 MB", level=LOG_LEVEL)

class DocumentHandler(FileSystemEventHandler):
    """Handles file system events for document processing"""
    
    def __init__(self):
        self.processed_files = set()
        self.processing_files = set()  # Track files currently being processed
    
    def on_created(self, event):
        """Handle new file creation"""
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        
        # Check if file is supported
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            logger.debug(f"Ignoring unsupported file: {file_path}")
            return
            
        # Avoid processing the same file multiple times
        if str(file_path) in self.processed_files or str(file_path) in self.processing_files:
            logger.debug(f"File already processed or processing: {file_path}")
            return
            
        # Mark as currently processing
        self.processing_files.add(str(file_path))
        
        # Wait for file to be completely written
        time.sleep(2)
        
        # Check if file still exists and is readable
        if not file_path.exists() or not file_path.is_file():
            logger.warning(f"File disappeared or is not readable: {file_path}")
            self.processing_files.discard(str(file_path))
            return
            
        logger.info(f"New document detected: {file_path}")
        self.process_document(file_path)
        
    def process_document(self, file_path: Path):
        """Process a new document through the simplified pipeline"""
        try:
            # Import directly to Paperless NGX
            self.import_to_paperless(file_path)
            
            # Mark as processed
            self.processed_files.add(str(file_path))
            self.processing_files.discard(str(file_path))
            
            logger.success(f"Successfully processed: {file_path.name}")
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
            # Remove from processing set to allow retry
            self.processing_files.discard(str(file_path))
    
    def import_to_paperless(self, file_path: Path):
        """Copy file to Paperless NGX consume folder"""
        consume_path = Path(PAPERLESS_CONSUME_FOLDER)
        consume_path.mkdir(exist_ok=True)
        
        target_path = consume_path / file_path.name
        
        # Handle filename conflicts
        counter = 1
        while target_path.exists():
            stem = file_path.stem
            suffix = file_path.suffix
            target_path = consume_path / f"{stem}_{counter}{suffix}"
            counter += 1
        
        # Copy file
        shutil.copy2(file_path, target_path)
        logger.info(f"Copied to Paperless consume folder: {target_path.name}")
        
        # Optional: Add metadata file for Paperless NGX
        self.create_metadata_file(target_path, file_path)
    
    def create_metadata_file(self, target_path: Path, source_path: Path):
        """Create optional metadata file for Paperless NGX"""
        try:
            metadata_path = target_path.with_suffix(target_path.suffix + '.json')
            metadata = {
                "title": source_path.stem,
                "created": time.strftime("%Y-%m-%d"),
                "source": "Nextcloud Auto-Import",
                "tags": ["auto-imported", "nautical-parts"]
            }
            
            import json
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
                
            logger.debug(f"Created metadata file: {metadata_path.name}")
            
        except Exception as e:
            logger.warning(f"Could not create metadata file: {str(e)}")

# FastAPI health check endpoint
app = FastAPI(title="Document Watcher Service")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "document-watcher"}

@app.get("/status")
async def get_status():
    return {
        "watch_folder": WATCH_FOLDER,
        "paperless_consume_folder": PAPERLESS_CONSUME_FOLDER,
        "supported_extensions": list(SUPPORTED_EXTENSIONS),
        "processed_files_count": len(event_handler.processed_files),
        "processing_files_count": len(event_handler.processing_files)
    }

@app.post("/force-process/{filename}")
async def force_process_file(filename: str):
    """Force process a specific file"""
    file_path = Path(WATCH_FOLDER) / filename
    
    if not file_path.exists():
        return {"error": f"File not found: {filename}"}
    
    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return {"error": f"Unsupported file type: {filename}"}
    
    try:
        event_handler.process_document(file_path)
        return {"success": f"File processed: {filename}"}
    except Exception as e:
        return {"error": f"Processing failed: {str(e)}"}

def start_health_server():
    """Start health check server in separate thread"""
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="warning")

def main():
    """Main function to start the document watcher"""
    global event_handler
    
    logger.info(f"Starting Document Watcher Service")
    logger.info(f"Watching folder: {WATCH_FOLDER}")
    logger.info(f"Paperless consume folder: {PAPERLESS_CONSUME_FOLDER}")
    
    # Ensure watch folder exists
    watch_path = Path(WATCH_FOLDER)
    if not watch_path.exists():
        logger.error(f"Watch folder does not exist: {WATCH_FOLDER}")
        return
    
    # Ensure consume folder exists
    consume_path = Path(PAPERLESS_CONSUME_FOLDER)
    consume_path.mkdir(exist_ok=True)
    
    # Setup file system watcher
    event_handler = DocumentHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=True)
    
    # Start health check server in background
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    
    # Start file watcher
    observer.start()
    logger.info("Document watcher started successfully")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping document watcher...")
        observer.stop()
    
    observer.join()
    logger.info("Document watcher stopped")

if __name__ == "__main__":
    main()