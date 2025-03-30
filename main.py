from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
from pathlib import Path
from llmClaude import identify_medical_equipment
from textToSpeech import text_to_speech_gtts
from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.responses import FileResponse

app = FastAPI()

@app.post("/identify-medical-equipment/")
async def identify_equipment(file: UploadFile = File(...)):
    """API endpoint to identify medical equipment from an uploaded image."""
    try:
        # Save uploaded file temporarily
        temp_file = f"temp_{file.filename}"
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Call the modular function
        result = identify_medical_equipment(
            image_path=temp_file,
            prompt="Name the medical equipment in this picture in one short phrase. No other text allowed."
        )
        
        # Clean up temp file
        Path(temp_file).unlink()
        
        return JSONResponse(content={"equipment_name": result}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/vocalize-equipment/")
async def vocalize_equipment(data: dict = Body(...)):
    try:
        equipment_name = data.get("equipment_name")
        if not isinstance(equipment_name, str):
            raise HTTPException(status_code=400, detail="equipment_name must be a string")

        audio_file = text_to_speech_gtts(equipment_name)
        return FileResponse(audio_file, media_type="audio/mpeg", filename="equipment_audio.mp3")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
 

# Run with: uvicorn api:app --reload
# Test ON GIT BASH: curl -X POST "http://127.0.0.1:8000/identify-medical-equipment/" \
#  -F "file=@C:\Users\14384\Desktop\test.jpeg"



