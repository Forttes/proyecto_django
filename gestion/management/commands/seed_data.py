import random
from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import transaction

from gestion.models import (
    Empresa, Area, TipoEquipo, EstadoOrden, Equipo,
    OrdenTrabajo, DetalleOrden,
)


class Command(BaseCommand):
    help = 'Carga datos masivos de prueba: 3 grupos, 3 usuarios, ~2000 registros'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('=== Creando grupos y usuarios ==='))

        # ── 1. Grupos ─────────────────────────────────────────
        grupo_admin, _ = Group.objects.get_or_create(name='admin_api')
        grupo_oper, _ = Group.objects.get_or_create(name='operador_api')
        grupo_sinrol, _ = Group.objects.get_or_create(name='sin_rol_api')

        # ── 2. Usuarios ───────────────────────────────────────
        usuarios_data = [
            ('admin_api', 'admin_api@demo.cl', 'AdminApi2026!', grupo_admin),
            ('operador_api', 'operador_api@demo.cl', 'OperadorApi2026!', grupo_oper),
            ('sin_rol_api', 'sin_rol_api@demo.cl', 'SinRolApi2026!', grupo_sinrol),
        ]

        for username, email, password, grupo in usuarios_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email, 'is_active': True,
                          'is_staff': False, 'is_superuser': False},
            )
            user.set_password(password)
            user.is_active = True
            user.is_staff = False
            user.is_superuser = False
            user.save()
            user.groups.set([grupo])
            self.stdout.write(f'  Usuario: {username} → grupo {grupo.name}')

        # ── 3. Catálogos base ────────────────────────────────
        self.stdout.write(self.style.WARNING('=== Creando catálogos ==='))

        empresas_nombres = [
            ('Minera del Norte S.A.', '76.111.111-1'),
            ('Constructora La Serena Ltda.', '76.222.222-2'),
            ('Agrícola Valle Verde SpA', '76.333.333-3'),
            ('Transportes del Pacífico S.A.', '76.444.444-4'),
            ('Servicios Eléctricos Chile Ltda.', '76.555.555-5'),
        ]
        empresas = []
        for nombre, rut in empresas_nombres:
            emp, _ = Empresa.objects.get_or_create(
                rut=rut,
                defaults={
                    'nombre': nombre,
                    'direccion': f'Av. Principal {random.randint(100, 9999)}',
                    'telefono': f'+56 51 {random.randint(200000, 299999)}',
                    'activo': True,
                },
            )
            empresas.append(emp)

        areas = []
        nombres_area = ['Mantención', 'Operaciones', 'Logística',
                        'Informática', 'Producción', 'Calidad',
                        'Seguridad', 'Administración']
        for emp in empresas:
            for na in random.sample(nombres_area, k=4):
                area, _ = Area.objects.get_or_create(nombre=na, empresa=emp)
                areas.append(area)

        tipos_equipo = []
        for nombre, desc in [
            ('Bomba', 'Equipo de bombeo industrial'),
            ('Compresor', 'Equipo de compresión de aire'),
            ('Motor', 'Motor eléctrico industrial'),
            ('Generador', 'Generador eléctrico'),
            ('Válvula', 'Válvula industrial'),
            ('Sensor', 'Sensor de monitoreo'),
            ('Torno', 'Torno mecánico'),
            ('Grúa', 'Grúa de levante'),
        ]:
            te, _ = TipoEquipo.objects.get_or_create(
                nombre=nombre, defaults={'descripcion': desc, 'activo': True},
            )
            tipos_equipo.append(te)

        estados_orden = []
        for nombre, desc in [
            ('Pendiente', 'Orden pendiente de ejecución'),
            ('En Proceso', 'Orden en ejecución'),
            ('Finalizada', 'Orden finalizada correctamente'),
            ('Cancelada', 'Orden cancelada por el usuario'),
            ('Atrasada', 'Orden fuera de plazo'),
        ]:
            eo, _ = EstadoOrden.objects.get_or_create(
                nombre=nombre, defaults={'descripcion': desc},
            )
            estados_orden.append(eo)

        # ── 4. Equipos (300) ─────────────────────────────────
        self.stdout.write(self.style.WARNING('=== Generando 300 equipos ==='))
        equipos = []
        for i in range(1, 301):
            codigo = f'EQ-{i:05d}'
            eq, _ = Equipo.objects.get_or_create(
                codigo=codigo,
                defaults={
                    'nombre': f'Equipo {i:03d}',
                    'tipo_equipo': random.choice(tipos_equipo),
                    'area': random.choice(areas),
                    'marca': random.choice(['Siemens', 'ABB', 'WEG', 'Schneider',
                                            'Caterpillar', 'Bosch']),
                    'modelo': f'MOD-{random.randint(100, 999)}',
                    'numero_serie': f'SN-{random.randint(100000, 999999)}',
                    'fecha_adquisicion': date(2020, 1, 1) +
                                         timedelta(days=random.randint(0, 1800)),
                    'activo': True,
                },
            )
            equipos.append(eq)

        # ── 5. Órdenes de trabajo (1000) ─────────────────────
        self.stdout.write(self.style.WARNING('=== Generando 1000 órdenes de trabajo ==='))
        admin_user = User.objects.get(username='admin_api')
        oper_user = User.objects.get(username='operador_api')

        prioridades = ['BAJA', 'MEDIA', 'ALTA', 'CRITICA']
        ordenes = []
        for i in range(1, 1001):
            numero = f'OT-{i:05d}'
            fecha_ini = date(2024, 1, 1) + timedelta(days=random.randint(0, 500))
            fecha_fin = None
            if random.random() > 0.4:
                fecha_fin = fecha_ini + timedelta(days=random.randint(1, 60))

            ot, _ = OrdenTrabajo.objects.get_or_create(
                numero_orden=numero,
                defaults={
                    'propietario': random.choice([admin_user, oper_user]),
                    'equipo': random.choice(equipos),
                    'estado': random.choice(estados_orden),
                    'descripcion': f'Trabajo de mantención #{i}',
                    'prioridad': random.choice(prioridades),
                    'fecha_inicio': fecha_ini,
                    'fecha_termino': fecha_fin,
                    'responsable': f'Técnico {random.randint(1, 30)}',
                    'observaciones': '',
                },
            )
            ordenes.append(ot)

        # ── 6. Detalles de orden (700) ───────────────────────
        self.stdout.write(self.style.WARNING('=== Generando 700 detalles de orden ==='))
        for i in range(700):
            orden = random.choice(ordenes)
            DetalleOrden.objects.create(
                orden=orden,
                actividad=f'Actividad {random.randint(1, 50)}: '
                          f'{random.choice(["Revisión", "Cambio", "Lubricación", "Ajuste", "Inspección"])}',
                horas_trabajo=Decimal(str(round(random.uniform(0.5, 8.0), 2))),
                observacion=random.choice(['', 'Sin novedades', 'Requiere repuesto']),
            )

        # ── 7. Resumen final ─────────────────────────────────
        total = (
            Empresa.objects.count() + Area.objects.count() +
            TipoEquipo.objects.count() + EstadoOrden.objects.count() +
            Equipo.objects.count() + OrdenTrabajo.objects.count() +
            DetalleOrden.objects.count()
        )

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=== CARGA COMPLETA ==='))
        self.stdout.write(f'Empresas:        {Empresa.objects.count()}')
        self.stdout.write(f'Áreas:           {Area.objects.count()}')
        self.stdout.write(f'Tipos de equipo: {TipoEquipo.objects.count()}')
        self.stdout.write(f'Estados de orden:{EstadoOrden.objects.count()}')
        self.stdout.write(f'Equipos:         {Equipo.objects.count()}')
        self.stdout.write(f'Órdenes:         {OrdenTrabajo.objects.count()}')
        self.stdout.write(f'Detalles:        {DetalleOrden.objects.count()}')
        self.stdout.write(self.style.SUCCESS(f'TOTAL REGISTROS: {total}'))
        self.stdout.write('')
        self.stdout.write('Usuarios creados:')
        self.stdout.write('  admin_api    / AdminApi2026!    (grupo admin_api)')
        self.stdout.write('  operador_api / OperadorApi2026! (grupo operador_api)')
        self.stdout.write('  sin_rol_api  / SinRolApi2026!   (grupo sin_rol_api)')