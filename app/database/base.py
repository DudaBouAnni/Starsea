from sqlalchemy.orm import declarative_base

Base = declarative_base()
"""
Classe base para todos os modelos do SQLAlchemy.

Todos as entidades devem herdar dessa classe.
Ela fornece o que é necessário para que as classes sejam mapeadas
para tabelas no banco de dados, permitindo criar, consultar, atualizar e
deletar registros usando SQLAlchemy.
"""