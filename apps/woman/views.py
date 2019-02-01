from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from .models import *
import bcrypt

def index(request):

	return render(request, 'woman/index.html')

def join(request):

	return render(request, 'woman/join.html')


def register(request):
	valid = User.objects.regValidator(request.POST)
	if len(valid):
		for k,v in valid.items():
			print(k,v)
			messages.error(request, v, extra_tags=k)
	else:
		hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email=request.POST['email'], password=hashedpw)
		user = User.objects.last()
		request.session['logged_in'] = user.id
		print(request.session['logged_in'])
		return redirect('/groups')

	return redirect('/join')

def login(request):
	msgs = User.objects.loginValidator(request.POST)
	if len(msgs):
		for k,v in msgs.items():
			print(k,v)
			messages.error(request, v, extra_tags=k)
	else:
		user = User.objects.get(email=request.POST['login_email'])
		request.session['logged_in'] = user.id
		return redirect('/groups')
	
	return redirect('/join')

def main_groups(request):
    if request.session['logged_in']:
        context={
            'user': User.objects.get(id=request.session['logged_in']),
            'group_data':Group.objects.all(),
            'group_new_title':Group.objects.last().group_title,
            'group_new_desc':Group.objects.last().group_desc,
            'group_new_id':Group.objects.last().id,
        }
    else:
        return redirect('/join')
    return render(request, 'woman/main_groups.html',context)

def groups(request,id):
    if request.session['logged_in']:
        context={
            'user': User.objects.get(id=request.session['logged_in']),
            'post_data':Post.objects.filter(groups_id=id),
            'comment_data':Comment.objects.filter(group_id=id),
            'group':Group.objects.get(id=id),
            'post_new_title':Post.objects.filter(groups_id=id).last().post_title,
            'post_new_post':Post.objects.filter(groups_id=id).last().post,

        }
    else:
        return redirect('/join')
    return render(request, 'woman/groups.html',context)

def add_groups(request):
    user = User.objects.get(id=request.session['logged_in'])
    context={
            'user':user,
    }
    if 'logged_in' not in request.session:
        return redirect('/join')
    else:
        if request.method== 'POST':
            msgs = Group.objects.groupValidator(request.POST)
            if len(msgs):
                for k,v in msgs.items():
                    print(k,v)
                    messages.error(request, v, extra_tags=k)
                return redirect('/add_group')
            Group.objects.create(group_title=request.POST['group_title'], group_desc=request.POST['group_desc'], created_by=User.objects.get(id=request.session['logged_in']))
            messages.success(request,'Group posted successfully.')
            return redirect('/groups')
    return render(request, 'woman/add_group.html',context)


def users(request,id):
    user=User.objects.get(id=id)
    data_post=user.uploader.all()
    data_group=user.creator.all()
    data_comment=user.u_comments.all()
    context={
        'user': user,
        'data_post':data_post,
        'data_group':data_group,
        'data_comment':data_comment
    }
    return render(request, 'woman/users.html',context)

def group_users(request,id):
    user=User.objects.get(id=id)
    data_post=user.uploader.all()
    data_group=user.creator.all()
    data_comment=user.u_comments.all()
    context={
        'user': user,
        'data_post':data_post,
        'data_group':data_group,
        'data_comment':data_comment
    }
    return render(request, 'woman/users.html',context)

def edit_group(request,id):
    user = User.objects.get(id=request.session['logged_in'])
    group = Group.objects.get(id=id)
    context={
            'user':user,
            'group':group
    }
    if request.method =='POST':
        msgs = Group.objects.updateGValidator(request.POST)
        if len(msgs):
            for k,v in msgs.items():
                print(k,v)
                messages.error(request, v, extra_tags=k)
                return redirect('/group/' + str(group.id))
        group = Group.objects.get(id=id)
        group_title = request.POST['update_group_title']
        group_desc = request.POST['update_group_desc']
        group.group_title = group_title
        group.group_desc = group_desc
        group.save()
        return redirect('/group/' + str(group.id))
    return render(request,"woman/edit_group.html",context)

def edit_post(request,id):
    user = User.objects.get(id=request.session['logged_in'])
    post = Post.objects.get(id=id)
    context={
            'user':user,
            'post':post
    }
    if request.method =='POST':
        msgs = Post.objects.updatePValidator(request.POST)
        if len(msgs):
            for k,v in msgs.items():
                print(k,v)
                messages.error(request, v, extra_tags=k)
                return redirect('/group/' + str(post.groups.id))
        post = Post.objects.get(id=id)
        # post_title = request.POST['update_post_title']
        # post = 
        post.post_title = request.POST['update_post_title']
        post.post = request.POST['update_post']
        post.save()
        return redirect('/group/' + str(post.groups.id))
    return render(request,"woman/edit_post.html",context)

def group_likes(request,id):
    group = Group.objects.get(id=id)
    context = {
        'likes':str(group.likes.all().count()),
        'group': group
    }
    print(group)
    groupToUpdate = Group.objects.get(id=id)
    current_user=request.session['logged_in']
    groupToUpdate.likes.add(current_user)
    groupToUpdate.save()
    return redirect('/groups',context)

def post_likes(request,id):
    post = Post.objects.get(id=id)
    context = {
        'liked':str(post.liked_by.all().count()),
        'post': post
    }
    print(post)
    postToUpdate = Post.objects.get(id=id)
    current_user=request.session['logged_in']
    postToUpdate.liked_by.add(current_user)
    postToUpdate.save()
    return redirect('/group/' + str(postToUpdate.groups_id))

def add_post(request,id):
    msgs = Post.objects.postValidator(request.POST)
    if len(msgs):
        for k,v in msgs.items():
            print(k,v)
            messages.error(request, v, extra_tags=k)
            return redirect('/group/'+ id)
    else:
        Post.objects.create(post=request.POST['post'],post_title=request.POST['post_title'], added_by=User.objects.get(id=request.session['logged_in']), groups=Group.objects.get(id=id))
        messages.success(request,'Message posted successfully.')
        return redirect('/group/'+ id)

def comment(request,id):
    groupFromPost = Post.objects.get(id=id).groups
    msgs = Comment.objects.commentValidator(request.POST)
    if len(msgs):
        for k,v in msgs.items():
            print(k,v)
            messages.error(request, v, extra_tags=k)
        return redirect('/group/'+str(groupFromPost.id))
    else:
        groupFromPost = Post.objects.get(id=id).groups
        Comment.objects.create(comment=request.POST['comment'],user=User.objects.get(id=request.session['logged_in']),post=Post.objects.get(id=id),group=groupFromPost)
    return redirect('/group/'+str(groupFromPost.id))

def delete_post(request,id):
    m = Post.objects.get(id=id)
    m.delete()
    return redirect('/group/'+ str(id))

def delete_comment(request,id):
    c = Comment.objects.get(id=id)
    group_id = c.group_id
    c.delete()
    return redirect('/group/'+ str(group_id))

def logout(request):
    request.session.clear()
    return redirect('/')