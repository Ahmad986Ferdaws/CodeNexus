pythonfrom typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_user_optional, get_db
from app.models.user import User
from app.schemas.snippet import (
    Comment, CommentCreate, Snippet, SnippetCreate, SnippetUpdate
)
from app.services.snippet import (
    create_comment, create_snippet, delete_snippet, get_snippet_by_id,
    get_snippets, update_snippet, add_view, add_like, remove_like
)

router = APIRouter()


@router.post("/", response_model=Snippet)
def create_new_snippet(
    *,
    db: Session = Depends(get_db),
    snippet_in: SnippetCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new snippet
    """
    return create_snippet(db, snippet_in, current_user.id)


@router.get("/", response_model=List[Snippet])
def read_snippets(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    language: Optional[str] = None,
    search: Optional[str] = Query(None),
    tags: Optional[List[str]] = Query(None),
    current_user: Optional[User] = Depends(get_current_user_optional)
) -> Any:
    """
    Retrieve snippets
    """
    return get_snippets(
        db,
        skip=skip,
        limit=limit,
        language=language,
        search=search,
        tags=tags,
        current_user_id=current_user.id if current_user else None
    )


@router.get("/{snippet_id}", response_model=Snippet)
def read_snippet(
    *,
    db: Session = Depends(get_db),
    snippet_id: UUID,
    current_user: Optional[User] = Depends(get_current_user_optional)
) -> Any:
    """
    Get snippet by ID
    """
    snippet = get_snippet_by_id(db, snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    
    # Check access to private snippets
    if not snippet.is_public and (not current_user or snippet.user_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to access this snippet")
    
    # Record view if user is not the owner
    if current_user and snippet.user_id != current_user.id:
        add_view(db, snippet)
    elif not current_user:
        add_view(db, snippet)
    
    return snippet


@router.put("/{snippet_id}", response_model=Snippet)
def update_snippet_endpoint(
    *,
    db: Session = Depends(get_db),
    snippet_id: UUID,
    snippet_in: SnippetUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update a snippet
    """
    snippet = get_snippet_by_id(db, snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    
    if snippet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this snippet")
    
    return update_snippet(db, snippet_id, snippet_in)


@router.delete("/{snippet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_snippet_endpoint(
    *,
    db: Session = Depends(get_db),
    snippet_id: UUID,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete a snippet
    """
    snippet = get_snippet_by_id(db, snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    
    if snippet.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to delete this snippet")
    
    delete_snippet(db, snippet_id)
    return None


@router.post("/{snippet_id}/comments", response_model=Comment)
def create_snippet_comment(
    *,
    db: Session = Depends(get_db),
    snippet_id: UUID,
    comment_in: CommentCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create a comment on a snippet
    """
    snippet = get_snippet_by_id(db, snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    
    return create_comment(db, snippet_id, comment_in, current_user.id)


@router.post("/{snippet_id}/like", response_model=Snippet)
def like_snippet_endpoint(
    *,
    db: Session = Depends(get_db),
    snippet_id: UUID,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Like a snippet
    """
    snippet = get_snippet_by_id(db, snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    
    return add_like(db, snippet, current_user.id)


@router.delete("/{snippet_id}/like", response_model=Snippet)
def unlike_snippet_endpoint(
    *,
    db: Session = Depends(get_db),
    snippet_id: UUID,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Remove like from a snippet
    """
    snippet = get_snippet_by_id(db, snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    
    return remove_like(db, snippet, current_user.id)
