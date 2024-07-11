import sqlite3
from django.contrib.auth.models import User, Permission
from django.db import connection
from datetime import date, timedelta
from random import randint
from core.models import Categoria, Producto, Carrito, Perfil, Boleta, DetalleBoleta, Bodega

def eliminar_tabla(nombre_tabla):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM {nombre_tabla}")
    conexion.commit()
    conexion.close()

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def crear_usuario(username, tipo, nombre, apellido, correo, es_superusuario, 
    es_staff, rut, direccion, subscrito, imagen):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'Superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='Duoc@123')
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='Duoc@123')

        if tipo == 'Administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'Administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()
 
        print(f'    Crear perfil: RUT {rut}, Subscrito {subscrito}, Imagen {imagen}')
        Perfil.objects.create(
            usuario=usuario, 
            tipo_usuario=tipo,
            rut=rut,
            direccion=direccion,
            subscrito=subscrito,
            imagen=imagen)
        print("    Creado correctamente")
    except Exception as err:
        print(f"    Error: {err}")

def eliminar_tablas():
    eliminar_tabla('auth_user_groups')
    eliminar_tabla('auth_user_user_permissions')
    eliminar_tabla('auth_group_permissions')
    eliminar_tabla('auth_group')
    eliminar_tabla('auth_permission')
    eliminar_tabla('django_admin_log')
    eliminar_tabla('django_content_type')
    #eliminar_tabla('django_migrations')
    eliminar_tabla('django_session')
    eliminar_tabla('Bodega')
    eliminar_tabla('DetalleBoleta')
    eliminar_tabla('Boleta')
    eliminar_tabla('Perfil')
    eliminar_tabla('Carrito')
    eliminar_tabla('Producto')
    eliminar_tabla('Categoria')
    #eliminar_tabla('authtoken_token')
    eliminar_tabla('auth_user')

def poblar_bd(test_user_email=''):
    eliminar_tablas()

    crear_usuario(
        username='wwhite',
        tipo='Cliente', 
        nombre='Walter', 
        apellido='White', 
        correo=test_user_email if test_user_email else 'wwhite@mcb.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='25.747.200-0',	
        direccion='308 Negra Arroyo Lane, Albuquerque, \nNuevo México 87001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/wwhite.jpg')

    crear_usuario(
        username='jpinkman',
        tipo='Cliente', 
        nombre='Jesse', 
        apellido='Pinkman', 
        correo=test_user_email if test_user_email else 'jpinkman@mcb.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='12.202.357-5', 
        direccion='9809 Margo Street, Albuquerque, \nNuevo México 87002 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/jpinkman.jpg')


    crear_usuario(
        username='gfring',
        tipo='Cliente', 
        nombre='Gus', 
        apellido='Fring', 
        correo=test_user_email if test_user_email else 'gfring@mcb.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='11.991.600-3', 
        direccion='13th Street Southwest, \nAlbuquerque, Nuevo México 87003 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/gfring.jpg')


    crear_usuario(
        username='tsalamanca',
        tipo='Cliente', 
        nombre='Tuco', 
        apellido='Salamanca', 
        correo=test_user_email if test_user_email else 'tsalamanca@mcb.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='16.469.725-8', 
        direccion='9th Street Southwest, \nAlbuquerque, Nuevo México 87004 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/tsalamanca.jpg')


    crear_usuario(
        username='aaguirre',
        tipo='Administrador', 
        nombre='Aoris', 
        apellido='Aguirre', 
        correo=test_user_email if test_user_email else 'aaguirre@mcb.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='20.189.245-0', 
        direccion='1900 Avenue of the Stars, \nCA90067 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/aaguirre.jpg')
    
    crear_usuario(
        username='efarias',
        tipo='Administrador', 
        nombre='Emanuel', 
        apellido='Farias', 
        correo=test_user_email if test_user_email else 'efarias@mcb.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='19.441.980-5', 
        direccion='5055 Wilshire Blvd., Los Angeles, \nCA 90036 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/efarias.jpg')

    crear_usuario(
        username='sgoodman',
        tipo='Superusuario',
        nombre='Saul',
        apellido='Goodman',
        correo=test_user_email if test_user_email else 'sgoodman@mcb.com',
        es_superusuario=True,
        es_staff=True,
        rut='13.029.317-4',
        direccion='12th Street Southwest, \nAlbuquerque, Nuevo México 87007 \nEstados Unidos',
        subscrito=False,
        imagen='perfiles/sgoodman.jpg')
    
    categorias_data = [
        { 'id': 1, 'nombre': 'Acción'},
        { 'id': 2, 'nombre': 'Aventura'},
        { 'id': 3, 'nombre': 'Estrategia'},
        { 'id': 4, 'nombre': 'RPG'},
    ]

    print('Crear categorías')
    for categoria in categorias_data:
        Categoria.objects.create(**categoria)
    print('Categorías creadas correctamente')

    productos_data = [
        # Categoría "Acción" (8 juegos)
        {
            'id': 1,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Devil May Cry 5',
            'descripcion': 'Un juego de acción y hack and slash donde los jugadores controlan a varios personajes, incluido Dante, en batallas estilizadas contra demonios.',
            'precio': 29990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000001.png'
        },
        {
            'id': 2,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Far Cry 6',
            'descripcion': 'Un juego de acción en primera persona que se desarrolla en un mundo abierto ficticio, donde los jugadores se enfrentan a un régimen opresivo en la isla de Yara utilizando armas y tácticas de guerrilla.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000002.png'
        },
        {
            'id': 3,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Borderlands 3',
            'descripcion': 'Un juego de disparos en primera persona con acción y elementos de RPG, donde los jugadores exploran mundos diferentes, recolectan botín y luchan contra enemigos en tiroteos frenéticos.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000003.png'
        },
        {
            'id': 4,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Nioh 2',
            'descripcion': 'Un juego de acción y RPG de samuráis donde los jugadores luchan contra yokais y otros enemigos en el Japón feudal, utilizando diferentes estilos de combate y habilidades especiales.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/000004.png'
        },
        {
            'id': 5,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Marvels Spider-Man',
            'descripcion': 'Un juego de acción y aventura donde los jugadores asumen el papel de Spider-Man, balanceándose por la ciudad de Nueva York y enfrentándose a enemigos como el Kingpin y el Doctor Octopus.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/000005.png'
        },
        {
            'id': 6,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Bayonetta 2',
            'descripcion': 'Un juego de acción y hack and slash donde los jugadores controlan a Bayonetta, una bruja con habilidades mágicas que lucha contra ángeles y demonios en batallas espectaculares.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000006.png'
        },
        {
            'id': 7,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Mortal Kombat 11',
            'descripcion': 'Un juego de lucha con acción intensa y combate brutal, conocido por sus gráficos detallados y movimientos especiales impactantes.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000007.png'
        },
        {
            'id': 8,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Resident Evil Village',
            'descripcion': 'Un juego de acción y survival horror donde los jugadores asumen el papel de Ethan Winters mientras explora un misterioso pueblo europeo lleno de horrores y enemigos grotescos.',
            'precio': 49990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000008.png'
        },
        # Categoría "Aventura" (4 juegos)
        {
            'id': 9,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'The Last of Us Part II',
            'descripcion': 'Un juego de acción y aventura que sigue la historia de Ellie en un mundo post-apocalíptico infestado de infectados, explorando temas profundos de venganza y supervivencia.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000009.png'
        },
        {
            'id': 10,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'A Plague Tale: Innocence',
            'descripcion': 'A Plague Tale: Innocence\' Un juego de aventura narrativa donde los jugadores guían a dos hermanos a través de una Francia medieval plagada de ratas y la Inquisición, enfrentando desafíos y tomando decisiones difíciles.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/000010.png'
        },
        {
            'id': 11,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Death Stranding',
            'descripcion': 'Un juego de aventura donde los jugadores asumen el papel de Sam Bridges, entregador en un mundo post-apocalíptico, explorando paisajes desolados y conectando comunidades aisladas.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000011.png'
        },
        {
            'id': 12,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Control',
            'descripcion': 'Un juego de aventura y acción con elementos sobrenaturales, donde los jugadores toman el papel de Jesse Faden, explorando un edificio en constante cambio lleno de secretos y poderes paranormales.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000012.png'
        },
        # Categoría "Estrategia" (4 juegos)
        {
            'id': 13,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Northgard',
            'descripcion': 'Un juego de estrategia en tiempo real donde los jugadores lideran un clan vikingo en la exploración, colonización y conquista de un nuevo continente, enfrentándose a desafíos naturales y rivales.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/000013.png'
        },
        {
            'id': 14,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Surviving Mars',
            'descripcion': 'Un juego de gestión y estrategia donde los jugadores deben construir y mantener una colonia en Marte, gestionando recursos, expansión y sobrevivencia de los colonos.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000014.png'
        },
        {
            'id': 15,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Iron Harvest',
            'descripcion': 'Un juego de estrategia en tiempo real ambientado en una realidad alternativa de la década de 1920, con mechs gigantes y tácticas de combate avanzadas.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000015.png'
        },
        {
            'id': 16,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Homeworld 3',
            'descripcion': 'La próxima entrega de la serie Homeworld, conocida por su enfoque en estrategia espacial y gestión de flotas en un entorno 3D.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000016.png'
        },
        # Categoría "RPG" (4 juegos)
        {
            'id': 17,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Sekiro: Shadows Die Twice',
            'descripcion': 'Juego del año - The Game Awards 2019 Mejor juego de acción de 2019 - IGN Traza tu propio camino hacia la venganza en la galardonada aventura de FromSoftware, creadores de Bloodborne y la saga Dark Souls. Véngate. Restituye tu honor. Mata con ingenio.',
            'precio': 29990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000017.png'
        },
        {
            'id': 18,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Monster Hunter Rise',
            'descripcion': 'Un RPG de acción donde los jugadores cazan monstruos en entornos diversos, utilizando una variedad de armas y habilidades.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/000018.png'
        },
        {
            'id': 19,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Wasteland 3',
            'descripcion': 'Un RPG táctico de mundo abierto con elementos de estrategia por turnos, ambientado en un mundo post-apocalíptico.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/000019.png'
        },
        {
            'id': 20,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'NieR Replicant ver.1.22474487139...',
            'descripcion': 'Una remasterización del clásico RPG de acción con una historia emocional y mecánicas de juego únicas.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/000020.png'
        }
    ]

    print('Crear productos')
    for producto in productos_data:
        Producto.objects.create(**producto)
    print('Productos creados correctamente')

    print('Crear carritos')
    for rut in ['25.747.200-0', '11.991.600-3']:
        cliente = Perfil.objects.get(rut=rut)
        for cantidad_productos in range(1, 11):
            producto = Producto.objects.get(pk=randint(1, 10))
            if cliente.subscrito:
                descuento_subscriptor = producto.descuento_subscriptor
            else:
                descuento_subscriptor = 0
            descuento_oferta = producto.descuento_oferta
            descuento_total = descuento_subscriptor + descuento_oferta
            descuentos = int(round(producto.precio * descuento_total / 100))
            precio_a_pagar = producto.precio - descuentos
            Carrito.objects.create(
                cliente=cliente,
                producto=producto,
                precio=producto.precio,
                descuento_subscriptor=descuento_subscriptor,
                descuento_oferta=descuento_oferta,
                descuento_total=descuento_total,
                descuentos=descuentos,
                precio_a_pagar=precio_a_pagar
            )
    print('Carritos creados correctamente')

    print('Crear boletas')
    nro_boleta = 0
    perfiles_cliente = Perfil.objects.filter(tipo_usuario='Cliente')
    for cliente in perfiles_cliente:
        estado_index = -1
        for cant_boletas in range(1, randint(6, 21)):
            nro_boleta += 1
            estado_index += 1
            if estado_index > 3:
                estado_index = 0
            estado = Boleta.ESTADO_CHOICES[estado_index][1]
            fecha_venta = date(2023, randint(1, 5), randint(1, 28))
            fecha_despacho = fecha_venta + timedelta(days=randint(0, 3))
            fecha_entrega = fecha_despacho + timedelta(days=randint(0, 3))
            if estado == 'Anulado':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Vendido':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Despachado':
                fecha_entrega = None
            boleta = Boleta.objects.create(
                nro_boleta=nro_boleta, 
                cliente=cliente,
                monto_sin_iva=0,
                iva=0,
                total_a_pagar=0,
                fecha_venta=fecha_venta,
                fecha_despacho=fecha_despacho,
                fecha_entrega=fecha_entrega,
                estado=estado)
            detalle_boleta = []
            total_a_pagar = 0
            for cant_productos in range(1, randint(4, 6)):
                producto_id = randint(1, 10)
                producto = Producto.objects.get(id=producto_id)
                precio = producto.precio
                descuento_subscriptor = 0
                if cliente.subscrito:
                    descuento_subscriptor = producto.descuento_subscriptor
                descuento_oferta = producto.descuento_oferta
                descuento_total = descuento_subscriptor + descuento_oferta
                descuentos = int(round(precio * descuento_total / 100))
                precio_a_pagar = precio - descuentos
                bodega = Bodega.objects.create(producto=producto)
                DetalleBoleta.objects.create(
                    boleta=boleta,
                    bodega=bodega,
                    precio=precio,
                    descuento_subscriptor=descuento_subscriptor,
                    descuento_oferta=descuento_oferta,
                    descuento_total=descuento_total,
                    descuentos=descuentos,
                    precio_a_pagar=precio_a_pagar)
                total_a_pagar += precio_a_pagar
            monto_sin_iva = int(round(total_a_pagar / 1.19))
            iva = total_a_pagar - monto_sin_iva
            boleta.monto_sin_iva = monto_sin_iva
            boleta.iva = iva
            boleta.total_a_pagar = total_a_pagar
            boleta.fecha_venta = fecha_venta
            boleta.fecha_despacho = fecha_despacho
            boleta.fecha_entrega = fecha_entrega
            boleta.estado = estado
            boleta.save()
            print(f'    Creada boleta Nro={nro_boleta} Cliente={cliente.usuario.first_name} {cliente.usuario.last_name}')
    print('Boletas creadas correctamente')

    print('Agregar productos a bodega')
    for producto_id in range(1, 11):
        producto = Producto.objects.get(id=producto_id)
        cantidad = 0
        for cantidad in range(1, randint(2, 31)):
            Bodega.objects.create(producto=producto)
        print(f'    Agregados {cantidad} "{producto.nombre}" a la bodega')
    print('Productos agregados a bodega')

