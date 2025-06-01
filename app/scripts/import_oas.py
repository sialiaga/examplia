import os
import sys
import argparse
import pandas as pd
from typing import Tuple
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.oa import OA
from app.db.session import SessionLocal

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("import_oas")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Import OAs from an Excel file')
    parser.add_argument(
        '--file',
        default='app/uploadable_files/oas.xlsx',
        help='Path to the Excel file containing OAs (relative to project root)'
    )
    return parser.parse_args()

def import_from_excel(file_path: str) -> Tuple[int, int, int]:
    """Import OAs from an Excel file.
    
    Args:
        file_path: Path to the Excel file
            
    Returns:
        tuple: (created_count, updated_count, error_count)
    """
    try:
        df = pd.read_excel(file_path)
        
        required_columns = ['curso', 'asignatura', 'unidad', 'codigo', 'OA']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

        df = df[required_columns]
        df = df.where(pd.notna(df), None)
        
        created_count = 0
        updated_count = 0
        error_count = 0
        
        db = SessionLocal()
        
        try:
            for _, row in df.iterrows():
                try:
                    curso = str(row['curso'])[:255] if row['curso'] is not None else ''
                    asignatura = str(row['asignatura'])[:255] if row['asignatura'] is not None else ''
                    unidad = str(row['unidad'])[:500] if row['unidad'] is not None else ''
                    codigo = str(row['codigo'])[:100] if row['codigo'] is not None else None
                    oa_text = str(row['OA']) if row['OA'] is not None else ""
                    
                    if not codigo or not oa_text:
                        error_count += 1
                        logger.warning(f"Skipping row with missing codigo or OA: {row}")
                        continue
                        
                    if not curso:
                        curso = 'No especificado'
                    if not asignatura:
                        asignatura = 'No especificado'
                    if not unidad:
                        unidad = 'No especificado'

                    existing_oa = db.query(OA).filter(OA.codigo == codigo).first()
                    
                    if existing_oa:
                        existing_oa.curso = curso
                        existing_oa.asignatura = asignatura
                        existing_oa.unidad = unidad
                        existing_oa.description = oa_text
                        updated_count += 1
                    else:
                        new_oa = OA(
                            curso=curso,
                            asignatura=asignatura,
                            unidad=unidad,
                            codigo=codigo,
                            description=oa_text
                        )
                        db.add(new_oa)
                        created_count += 1
                        
                except Exception as e:
                    error_count += 1
                    logger.error(
                        f"Error processing row with codigo {row.get('codigo', 'unknown')}:\nError: {str(e)}"
                    )

            db.commit()
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
            
        return created_count, updated_count, error_count
            
    except Exception as e:
        logger.error(f"Error importing Excel file: {str(e)}")
        raise

def main():
    """Main entry point for the script."""
    args = parse_arguments()
    file_path = args.file
    
    if not os.path.isabs(file_path):
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        absolute_path = os.path.join(project_root, file_path)
    else:
        absolute_path = file_path
    
    if not os.path.exists(absolute_path):
        logger.error(f"File {absolute_path} does not exist")
        sys.exit(1)
    
    logger.info(f"Importing OAs from {absolute_path}")
    
    try:
        created_count, updated_count, error_count = import_from_excel(absolute_path)
        
        logger.info(
            f"Import completed: {created_count} OAs created, {updated_count} OAs updated, {error_count} errors."
        )
        
    except Exception as e:
        logger.error(f"Error importing Excel file: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
