from fastapi import APIRouter, Depends, status

from src.models.user import User
from src.schemas.transaction import TransactionCreate, TransactionRead
from src.security import get_current_user
from src.services.transaction import TransactionService

router = APIRouter()


@router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(),
):
    """
    Cria uma nova transação (depósito ou saque).

    A lógica de serviço garantirá que o usuário autenticado seja o dono da conta.
    """
    return await service.create_transaction(user_id=current_user.id, transaction_data=transaction_data)
