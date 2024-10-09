import unittest
import json
from app import create_app, db
from app.models.compras import Compras
from datetime import datetime

class TestComprasRoutes(unittest.TestCase):

    def setUp(self):
        # Crear la aplicación de prueba
        self.app = create_app() 
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_compra(self):
        data = {
            'producto_id': 1,
            'direccion_envio': 'Calle Falsa 123'
        }
        response = self.client.post('/compras/', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        json_data = json.loads(response.data)
        self.assertEqual(json_data['producto_id'], 1)
        self.assertEqual(json_data['direccion_envio'], 'Calle Falsa 123')

    def test_get_compra(self):
        compra = Compras.crear_compra(producto_id=1, direccion_envio='Calle Falsa 123')

        response = self.client.get(f'/compras/{compra.id}')
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)
        self.assertEqual(json_data['producto_id'], 1)
        self.assertEqual(json_data['direccion_envio'], 'Calle Falsa 123')

    def test_get_compras(self):
        compra1 = Compras.crear_compra(producto_id=1, direccion_envio='Calle 1')
        compra2 = Compras.crear_compra(producto_id=2, direccion_envio='Calle 2')

        response = self.client.get('/compras/')
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data)
        self.assertEqual(len(json_data), 2)
        self.assertEqual(json_data[0]['producto_id'], 1)
        self.assertEqual(json_data[1]['producto_id'], 2)

    def test_update_compra(self):
        compra = Compras.crear_compra(producto_id=1, direccion_envio='Calle Falsa 123')

        update_data = {
            'producto_id': 2,
            'direccion_envio': 'Calle Actualizada 456'
        }

        response = self.client.put(f'/compras/{compra.id}', data=json.dumps(update_data), content_type='application/json') #Actualiza compras
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.data) #Verificación actualización
        self.assertEqual(json_data['producto_id'], 2)
        self.assertEqual(json_data['direccion_envio'], 'Calle Actualizada 456')

    def test_delete_compra(self):
        compra = Compras.crear_compra(producto_id=1, direccion_envio='Calle Falsa 123')
        # Eliminar la compra a través de la API
        response = self.client.delete(f'/compras/{compra.id}')
        self.assertEqual(response.status_code, 200)
        # Verificar que la compra haya sido eliminada
        self.assertEqual(Compras.query.count(), 0)

if __name__ == '__main__':
    unittest.main()