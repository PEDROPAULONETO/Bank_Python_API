from typing import List

from fastapi import APIRouter, Depends, status

from src.models.user import User
from src.schemas.account import AccountCreate, AccountRead
from src.schemas.transaction import TransactionRead
from src.security import get_current_user
from src.services.account import AccountService

router = APIRouter()


@router.post("/", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
async def create_account(
    account_data: AccountCreate,
    current_user: User = Depends(get_current_user),
    service: AccountService = Depends(),
):
    """Cria uma nova conta para o usuário autenticado."""
    return await service.create_account(user_id=current_user.id, account_data=account_data)


@router.get("/", response_model=List[AccountRead])
async def list_accounts(
    current_user: User = Depends(get_current_user),
    service: AccountService = Depends(),
):
    """Lista todas as contas pertencentes ao usuário autenticado."""
    return await service.get_accounts_by_user(user_id=current_user.id)


@router.get("/{account_id}/transactions", response_model=List[TransactionRead])
async def list_account_transactions(
    account_id: int,
    current_user: User = Depends(get_current_user),
    service: AccountService = Depends(),
):
    """
    Lista as transações de uma conta específica.

    Garante que a conta pertence ao usuário autenticado antes de retornar os dados.
    """
    return await service.get_account_transactions(user_id=current_user.id, account_id=account_id)
