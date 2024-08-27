from django.contrib.auth.models import User
from django.test import TestCase
from .models import Post
from django.shortcuts import reverse


# Create your tests here.


class BlogPostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='user1')

        cls.post1 = Post.objects.create(
            title='post1',
            text='this is a description',
            status=Post.STATUS_CHOICES[0][0],  # publish
            author=cls.user
        )
        cls.post2 = Post.objects.create(
            title='post2',
            text='lorem ipsum',
            status=Post.STATUS_CHOICES[1][0],  # draft
            author=cls.user
        )

    # def setUp(self):
    #     self.user = User.objects.create(username='user1')
    #
    #     self.post1 =  Post.objects.create(
    #         title = 'post1',
    #         text = 'this is a description',
    #         status = Post.STATUS_CHOICES[0][0],#publish
    #         author = self.user,
    #     )
    #     self.post2 = Post.objects.create(
    #         title = 'post2',
    #         text = 'lorem ipsum',
    #         status = Post.STATUS_CHOICES[1][0],#draft
    #         author = self.user
    #     )
    def test_post_model_str(self):
        post = self.post1
        self.assertEqual(str(post), post.title)


    def test_post_detail(self):
        self.assertEqual(self.post1.title, 'post1')
        self.assertEqual(self.post1.text, 'this is a description')


    def test_post_list_url(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)


    def test_post_list_url_by_name(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_title_on_blog_list(self):
        response = self.client.get(reverse('post_list'))
        self.assertContains(response , self.post1.title)

    def test_post_detail_url(self):
        response = self.client.get(f'/blog/{self.post1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_url_by_name(self):
        response = self.client.get(reverse('post_detail' , args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_details_on_blog_detail_page(self):
        response = self.client.get(reverse('post_detail' , args=[self.post1.id]))
        self.assertContains(response , self.post1.title)
        self.assertContains(response , self.post1.text)

    def test_status_404_if_id_not_exist(self):
        response = self.client.get(reverse('post_detail', args=[999]))
        self.assertEqual(response.status_code , 404)


    def test_draft_post(self):
        response = self.client.get(reverse('post_list'))
        self.assertContains(response , self.post1.title)
        self.assertNotContains(response , self.post2.title)


    def test_post_crate_view(self):
        response = self.client.post(reverse('post_create'),{
            'title':'some title',
            'text':'some text',
            'status': 'pub',
            'author': self.user.id,

        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title , 'some title')
        self.assertEqual(Post.objects.last().text , 'some text')

    def test_post_edit_view(self):
        response = self.client.post(reverse('post_update' , args=[self.post2.id]),{
            'title':'Post1 title updated',
            'text':'Post1 text updated',
            'status': 'pub',
            'author': self.post2.author.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title , 'Post1 title updated')
        self.assertEqual(Post.objects.last().text , 'Post1 text updated')


    def post_delete_view(self):
        response = self.client.post(reverse('post_delete' , args=[self.post2.id]))
        self.assertEqual(response.status_code, 302)