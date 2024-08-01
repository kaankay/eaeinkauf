import datetime
from django.test import TestCase
from weaeinkauf.models import Quelle
from weaeinkauf.views import getAllQuelles


class QuelleTest(TestCase):
    def setUp(self):
        Quelle.objects.create(
            alt_id=1, name='test_quelle', quellendatum = datetime.datetime.now().date(),
            bemerkung = 'test_bemerkung',
            created_by='test_creator' 

        )
        Quelle.objects.create(
            alt_id=2, name='test_quelle2', quellendatum = datetime.datetime.now().date(),
            bemerkung = 'test_bemerkung2',
            created_by='test_creator2',
            quellenart='Vertrag'

        )
        return super().setUp()
    
    def test_quelle_exists(self):
        quelle = Quelle.objects.get(alt_id=1)
        self.assertEqual(quelle.alt_id, 1)
        self.assertEqual(quelle.name, 'test_quelle')
        self.assertEqual(quelle.quellendatum, datetime.datetime.now().date())
        self.assertEqual(quelle.bemerkung, 'test_bemerkung',)
        self.assertEqual(quelle.created_by, 'test_creator' )
        self.assertEqual(quelle.quellenart, 'Angebot')
    
    def test_getAllQuelles(self):
        all_quelles = getAllQuelles(None, None)
        self.assertEqual(len(all_quelles), 2)
    
    def test_getAllQuelles_only_Angebot(self):
        all_quelles = getAllQuelles('Angebot', None)
        quelle = Quelle.objects.first()
        self.assertEqual(len(all_quelles), 1)
        self.assertEqual(quelle.quellenart, 'Angebot')
    
    def test_getAllQuelles_only_Vertrag(self):
        all_quelles = getAllQuelles('Vertrag', None)
        quelle = all_quelles.first()
        self.assertEqual(len(all_quelles), 1)
        self.assertEqual(quelle.quellenart, 'Vertrag')
