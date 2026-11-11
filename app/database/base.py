from sqlalchemy.orm import declarative_base

Base = declarative_base()
"""
Classe base de todos os modelos SQLAlchemy.

Todas as entidades devem herdar desta classe.
Permite mapear classes para tabelas e criar, consultar, atualizar e excluir registros.
"""
