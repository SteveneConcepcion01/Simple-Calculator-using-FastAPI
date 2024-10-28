from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


class Operation(BaseModel):
    num1: float
    num2: float
    operation: str  


class OperationResult(BaseModel):
    operation_str: str
    result: float


operation_history: List[OperationResult] = []

@app.post("/calculate")
async def calculate(operation: Operation):
    
    if operation.operation == "add":
        result = operation.num1 + operation.num2
        operation_str = f"{operation.num1} + {operation.num2} = {result}"
    elif operation.operation == "subtract":
        result = operation.num1 - operation.num2
        operation_str = f"{operation.num1} - {operation.num2} = {result}"
    elif operation.operation == "multiply":
        result = operation.num1 * operation.num2
        operation_str = f"{operation.num1} * {operation.num2} = {result}"
    elif operation.operation == "divide":
        if operation.num2 == 0:
            raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
        result = operation.num1 / operation.num2
        operation_str = f"{operation.num1} / {operation.num2} = {result}"
    else:
        raise HTTPException(status_code=400, detail="Invalid operation type. Choose 'add', 'subtract', 'multiply', or 'divide'.")

    
    operation_history.append(OperationResult(operation_str=operation_str, result=result))
    return {"operation": operation_str, "result": result}

@app.get("/history")
async def get_history():
    
    return {"history": operation_history}
