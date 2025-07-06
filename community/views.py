from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, BoardType
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User

# 게시글 목록 (이미 구현되어 있다면 생략)
def post_list(request, board_type):
    posts = Post.objects.filter(board_type=board_type).order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    board_name = dict(BoardType.choices)[board_type]
    context = {
        'posts': page_obj,
        'board_type': board_type,
        'board_name': board_name,
    }
    return render(request, 'community/post_list.html', context)

# 게시글 상세
def post_detail(request, board_type, pk):
    post = get_object_or_404(Post, pk=pk, board_type=board_type)
    return render(request, 'community/post_detail.html', {'post': post})

# 글쓰기
@login_required
def post_create(request, board_type):
    # 권한 체크: 개발과정만 daddy, juan만 허용
    if board_type == 'development' and request.user.username not in ['daddy', 'juan']:
        return HttpResponseForbidden("개발과정 게시판은 관리자만 글을 쓸 수 있습니다.")
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        post = Post.objects.create(
            board_type=board_type,
            title=title,
            content=content,
            author=request.user,
        )
        messages.success(request, '글이 등록되었습니다.')
        return redirect('post_detail', board_type=board_type, pk=post.pk)
    return render(request, 'community/post_form.html', {'board_type': board_type, 'mode': 'create'})

# 글수정
@login_required
def post_edit(request, board_type, pk):
    post = get_object_or_404(Post, pk=pk, board_type=board_type)
    # 권한 체크
    if board_type == 'development' and request.user.username not in ['daddy', 'juan']:
        return HttpResponseForbidden("개발과정 게시판은 관리자만 수정할 수 있습니다.")
    if request.user != post.author:
        return HttpResponseForbidden("작성자만 수정할 수 있습니다.")
    if request.method == 'POST':
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.save()
        messages.success(request, '글이 수정되었습니다.')
        return redirect('post_detail', board_type=board_type, pk=post.pk)
    return render(request, 'community/post_form.html', {'post': post, 'board_type': board_type, 'mode': 'edit'})

# 글삭제
@login_required
def post_delete(request, board_type, pk):
    post = get_object_or_404(Post, pk=pk, board_type=board_type)
    # 권한 체크
    if board_type == 'development' and request.user.username not in ['daddy', 'juan']:
        return HttpResponseForbidden("개발과정 게시판은 관리자만 삭제할 수 있습니다.")
    if request.user != post.author:
        return HttpResponseForbidden("작성자만 삭제할 수 있습니다.")
    if request.method == 'POST':
        post.delete()
        messages.success(request, '글이 삭제되었습니다.')
        return redirect('post_list', board_type=board_type)
    return render(request, 'community/post_confirm_delete.html', {'post': post, 'board_type': board_type})
