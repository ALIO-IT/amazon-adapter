"""
Amazon Adapter - FastAPI Application
Converts AutoZone-style auto parts CSV to Amazon upload format
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from adapter.csv_parser import AutoPartsParser
from adapter.amazon_transformer import AmazonTransformer

app = FastAPI(
    title="Amazon Auto Parts Adapter",
    description="Convert AutoZone-style auto parts CSV to Amazon upload format",
    version="1.0.0"
)

# CORS middleware for web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the web interface"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Amazon Auto Parts Adapter</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                padding: 40px;
                max-width: 600px;
                width: 100%;
            }
            
            h1 {
                color: #333;
                margin-bottom: 10px;
                font-size: 28px;
                text-align: center;
            }
            
            .subtitle {
                color: #666;
                text-align: center;
                margin-bottom: 30px;
                font-size: 14px;
            }
            
            .upload-area {
                border: 3px dashed #667eea;
                border-radius: 10px;
                padding: 40px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-bottom: 20px;
            }
            
            .upload-area:hover {
                border-color: #764ba2;
                background: #f8f9ff;
            }
            
            .upload-area.dragover {
                border-color: #764ba2;
                background: #f0f0ff;
            }
            
            .upload-icon {
                font-size: 48px;
                margin-bottom: 15px;
            }
            
            input[type="file"] {
                display: none;
            }
            
            .btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 25px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 600;
                transition: transform 0.2s;
                width: 100%;
                margin-top: 10px;
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            
            .btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            
            #status {
                margin-top: 20px;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                display: none;
            }
            
            .success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            
            .error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            
            .info {
                background: #d1ecf1;
                color: #0c5460;
                border: 1px solid #bee5eb;
            }
            
            .loading {
                display: none;
                margin-top: 20px;
                text-align: center;
            }
            
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .file-info {
                background: #f8f9ff;
                padding: 15px;
                border-radius: 8px;
                margin-top: 15px;
                display: none;
            }
            
            .file-info p {
                color: #333;
                margin: 5px 0;
            }
            
            .download-btn {
                background: #28a745;
                margin-top: 15px;
            }
            
            .download-btn:hover {
                box-shadow: 0 5px 15px rgba(40, 167, 69, 0.4);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚗 Amazon Auto Parts Adapter</h1>
            <p class="subtitle">Convert AutoZone CSV to Amazon format</p>
            
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">📁</div>
                <p style="color: #667eea; font-weight: 600; margin-bottom: 8px;">
                    Drag & drop your CSV file here
                </p>
                <p style="color: #999; font-size: 14px;">or click to browse</p>
                <input type="file" id="fileInput" accept=".csv" />
            </div>
            
            <div class="file-info" id="fileInfo"></div>
            
            <button class="btn" id="convertBtn" disabled>Convert to Amazon Format</button>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p style="margin-top: 10px; color: #667eea;">Processing your file...</p>
            </div>
            
            <div id="status"></div>
            
            <button class="btn download-btn" id="downloadBtn" style="display: none;">
                Download Amazon CSV
            </button>
        </div>
        
        <script>
            const uploadArea = document.getElementById('uploadArea');
            const fileInput = document.getElementById('fileInput');
            const convertBtn = document.getElementById('convertBtn');
            const downloadBtn = document.getElementById('downloadBtn');
            const status = document.getElementById('status');
            const loading = document.getElementById('loading');
            const fileInfo = document.getElementById('fileInfo');
            let selectedFile = null;
            let outputFileName = null;
            
            uploadArea.addEventListener('click', () => fileInput.click());
            
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });
            
            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragover');
            });
            
            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    handleFile(files[0]);
                }
            });
            
            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    handleFile(e.target.files[0]);
                }
            });
            
            function handleFile(file) {
                if (!file.name.endsWith('.csv')) {
                    showStatus('Please select a CSV file', 'error');
                    return;
                }
                
                selectedFile = file;
                convertBtn.disabled = false;
                fileInfo.style.display = 'block';
                fileInfo.innerHTML = `
                    <p><strong>File:</strong> ${file.name}</p>
                    <p><strong>Size:</strong> ${(file.size / 1024).toFixed(2)} KB</p>
                `;
                showStatus('File loaded successfully! Click "Convert" to process.', 'info');
                downloadBtn.style.display = 'none';
            }
            
            convertBtn.addEventListener('click', async () => {
                if (!selectedFile) return;
                
                const formData = new FormData();
                formData.append('file', selectedFile);
                
                convertBtn.disabled = true;
                loading.style.display = 'block';
                status.style.display = 'none';
                downloadBtn.style.display = 'none';
                
                try {
                    const response = await fetch('/convert', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        outputFileName = data.output_file;
                        showStatus(
                            `✅ Success! Processed ${data.rows_processed} rows. ${data.message}`,
                            'success'
                        );
                        downloadBtn.style.display = 'block';
                    } else {
                        showStatus(`❌ Error: ${data.detail}`, 'error');
                        convertBtn.disabled = false;
                    }
                } catch (error) {
                    showStatus(`❌ Error: ${error.message}`, 'error');
                    convertBtn.disabled = false;
                } finally {
                    loading.style.display = 'none';
                }
            });
            
            downloadBtn.addEventListener('click', async () => {
                if (!outputFileName) return;
                
                window.location.href = `/download/${outputFileName}`;
            });
            
            function showStatus(message, type) {
                status.textContent = message;
                status.className = type;
                status.style.display = 'block';
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/convert")
async def convert_csv(file: UploadFile = File(...)):
    """
    Convert uploaded AutoZone-style CSV to Amazon format
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")
    
    try:
        # Read uploaded file
        contents = await file.read()
        
        # Parse the AutoZone CSV
        parser = AutoPartsParser()
        df = parser.parse(contents)
        
        # Transform to Amazon format
        transformer = AmazonTransformer()
        amazon_df = transformer.transform(df)
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"amazon_auto_parts_{timestamp}.csv"
        output_path = OUTPUT_DIR / output_filename
        
        # Save the Amazon-formatted CSV
        amazon_df.to_csv(output_path, index=False)
        
        return {
            "message": "File converted successfully",
            "output_file": output_filename,
            "rows_processed": len(df),
            "rows_output": len(amazon_df)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.get("/download/{filename}")
async def download_file(filename: str):
    """
    Download the converted Amazon CSV file
    """
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="text/csv"
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Amazon Auto Parts Adapter"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

