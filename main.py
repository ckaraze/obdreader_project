from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import obd
from datetime import datetime, timezone

# Create an instance of the FastAPI
app = FastAPI()

# Create a connection to the OBD-II adapter
connection = obd.OBD()

# Define a Pydantic model for error codes
class ErrorCode(BaseModel):
    code: str
    description: str
    timestamp: str

# Define a Pydantic model for the response
class CarInfo(BaseModel):
    vin: Optional[str]
    speed: Optional[float]
    rpm: Optional[float]
    throttle_position: Optional[float]
    error_codes: List[Optional[ErrorCode]]

@app.get("/carinfo", response_model=CarInfo)
def read_car_info():
    try:
        # Query the car for VIN
        vin_cmd = obd.commands.VIN
        vin_resp = connection.query(vin_cmd)
        vin = vin_resp.value.strip() if vin_resp.value else None

        # Query the car for speed
        speed_cmd = obd.commands.SPEED
        speed_resp = connection.query(speed_cmd)
        speed = speed_resp.value.magnitude if speed_resp.value else None

        # Query the car for RPM
        rpm_cmd = obd.commands.RPM
        rpm_resp = connection.query(rpm_cmd)
        rpm = rpm_resp.value.magnitude if rpm_resp.value else None

        # Query the car for throttle position
        throttle_cmd = obd.commands.THROTTLE_POS
        throttle_resp = connection.query(throttle_cmd)
        throttle_position = throttle_resp.value.magnitude if throttle_resp.value else None

        # Query the car for error codes
        dtc_cmd = obd.commands.GET_DTC
        dtc_resp = connection.query(dtc_cmd)
        timestamp = datetime.now(timezone.utc).isoformat()
        error_codes = [ErrorCode(code=code[0], description=code[1], timestamp=timestamp) for code in dtc_resp.value] if dtc_resp.value else []

        # Create the CarInfo object
        car_info = CarInfo(
            speed=speed,
            rpm=rpm,
            throttle_position=throttle_position,
            vin=vin,
            error_codes = error_codes
        )

        return car_info

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)