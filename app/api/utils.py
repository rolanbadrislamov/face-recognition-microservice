def userEntity(entity)-> dict:
    return {
        "id": str(entity["id"]),
        "username": entity.username,
        "email": entity.email,
        "role": entity.role,
        "created_at": entity.created_at,
        "updated_at": entity.updated_at,
    }