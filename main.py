from fastapi import FastAPI, HTTPException
from sandl import Parser

app = FastAPI()

parser = Parser()

@app.post("/parse/")
async def parse_input(input_string: str):
    try:
        # Parse the input string
        parser.parse(input_string)
        # Get the parsing table
        table_json = parser.get_table()
        return {"table_json": table_json}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing input: {str(e)}")
    
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)