from fastapi import APIRouter, Depends, HTTPException

from src.adapters.notifications.schemas import NotificationCreate
from src.services.notifications import NotificationService

router = APIRouter(prefix='/notifications', tags=['notifications'])


@router.post('/')
async def create_notification(data: NotificationCreate, service: NotificationService = Depends()):
    """Создаёт нотификацию для пользователя"""
    try:
        notification = await service.create_notification(
            user_uid=data.user_uid, content=data.content, channel=data.channel
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'uid': str(notification.uid), 'status': notification.status.name}
