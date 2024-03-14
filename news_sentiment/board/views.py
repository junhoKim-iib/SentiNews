from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.db.models import Count

class PostListView(View):
    
    def get(self, request):
        posts = Post.objects.annotate(comment_count=Count('comment')).order_by('-created_at')
        paginator = Paginator(posts, 10)  # Show 10 posts per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'posts': posts,

        }
        
        return render(request, 'board/post_list.html', context)


class PostCreateView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = PostForm()
        return render(request, 'board/post_create.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('board:post_detail', pk=post.pk)
        return render(request, 'board/post_create.html', {'form': form})


class PostDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(post=post)

        # 조회수 증가
        post.view_count += 1
        post.save()

        context = {
            'post': post,
            'comments': comments,
            'user': request.user,
        }
        return render(request, 'board/post_detail.html', context)


class PostDeleteView(View):
    @method_decorator(login_required)
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('board:post_list')

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'board/post_delete.html', {'post': post})


class PostEditView(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = PostForm(instance=post)
        context = {
            'form': form,
            'post': post,
        }
        return render(request, 'board/post_edit.html', context)

    @method_decorator(login_required)
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('board:post_detail', pk=post.pk)
        return render(request, 'board/post_edit.html', {'form': form})


class CommentCreateView(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        return render(request, 'board/comment_create.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('board:post_detail', pk=post.pk)
        return render(request, 'board/comment_create.html', {'form': form})


class CommentDeleteView(View):
    @method_decorator(login_required)
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if request.user != comment.author:
            return JsonResponse({'error': '댓글을 삭제할 권한이 없습니다.'}, status=403)

        comment.delete()

        return JsonResponse({'success': '댓글이 성공적으로 삭제되었습니다.'})


class CommentEditView(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        form = CommentForm(instance=comment)
        return render(request, 'board/comment_edit.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        post_pk = comment.post.pk
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            return redirect('board:post_detail', pk=post_pk)
        return render(request, 'board/comment_edit.html', {'form': form})
