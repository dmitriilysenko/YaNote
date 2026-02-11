from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note

User = get_user_model()

class TestDetailPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Пупсик')
        notes = []
        for index in range(5):
            notes.append(
                Note(
                    title=f'Тестовая заметка {index + 1}',
                    text='Просто текст заметки.',
                    author=cls.author,
                    slug=f'slug-{index + 1}',
                )
            )
        Note.objects.bulk_create(notes)

    def test_notes_order(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('notes:list'))
        self.assertIn('object_list', response.context)
        notes_in_context = response.context['object_list']
        list_ids = [note.id for note in notes_in_context]
        
        # 4. Создаём отсортированный список id (по возрастанию)
        sorted_ids = sorted(list_ids)
        
        # 5. Сравниваем: если порядок совпадает — сортировка верна
        self.assertEqual(list_ids, sorted_ids, 'Заметки должны быть отсортированы по id (от меньшего к большему)')