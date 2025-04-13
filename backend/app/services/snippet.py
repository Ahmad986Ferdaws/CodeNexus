from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.snippet import CodeSnippet, Comment
from app.schemas.snippet import CommentCreate, SnippetCreate, SnippetUpdate


def get_snippets(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    language: Optional[str] = None,
    search: Optional[str] = None,
    tags: Optional[List[str]] = None,
    current_user_id: Optional[UUID] = None
) -> List[CodeSnippet]:
    """Get all snippets with filters"""
    query = db.query(CodeSnippet)
    
    # Filter by public or user's own snippets
    if current_user_id:
        query = query.filter(
            or_(
                CodeSnippet.is_public == True,
                CodeSnippet.user_id == current_user_id
            )
        )
    else:
        query = query.filter(CodeSnippet.is_public == True)
    
    # Apply language filter
    if language:
        query = query.filter(CodeSnippet.language == language)
    
    # Apply search filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                CodeSnippet.title.ilike(search_term),
                CodeSnippet.description.ilike(search_term),
                CodeSnippet.code.ilike(search_term)
            )
        )
    
    # Apply tags filter
    if tags:
        for tag in tags:
            query = query.filter(CodeSnippet.tags.contains([tag]))
    
    # Order by creation date (newest first)
    query = query.order_by(CodeSnippet.created_at.desc())
    
    return query.offset(skip).limit(limit).all()


def get_snippet_by_id(db: Session, snippet_id: UUID) -> Optional[CodeSnippet]:
    """Get a specific snippet by ID"""
    return db.query(CodeSnippet).filter(CodeSnippet.id == snippet_id).first()


def create_snippet(db: Session, snippet_in: SnippetCreate, user_id: UUID) -> CodeSnippet:
    """Create a new snippet"""
    snippet = CodeSnippet(
        **snippet_in.dict(),
        user_id=user_id
    )
    db.add(snippet)
    db.commit()
    db.refresh(snippet)
    return snippet


def update_snippet(db: Session, snippet_id: UUID, snippet_in: SnippetUpdate) -> CodeSnippet:
    """Update a snippet"""
    snippet = get_snippet_by_id(db, snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    
    update_data = snippet_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(snippet, field, value
