from rest_framework import serializers
from .models import (
    Empresa,
    Area,
    TipoEquipo,
    EstadoOrden,
    Equipo,
    OrdenTrabajo,
    DetalleOrden,
)


# ─────────────────────────────────────────────────────────────
# Serializers — modelos principales
# ─────────────────────────────────────────────────────────────

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['id', 'nombre', 'rut', 'direccion', 'telefono', 'activo']

    def validate_rut(self, value):
        """Validación de campo: RUT no puede ser vacío ni muy corto."""
        if len(value.strip()) < 8:
            raise serializers.ValidationError(
                'El RUT debe tener al menos 8 caracteres.'
            )
        return value


class AreaSerializer(serializers.ModelSerializer):
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)

    class Meta:
        model = Area
        fields = ['id', 'nombre', 'empresa', 'empresa_nombre', 'activo']

    def validate(self, data):
        """Validación de relación: no puede haber dos áreas con el mismo nombre
        en la misma empresa."""
        nombre = data.get('nombre')
        empresa = data.get('empresa')
        qs = Area.objects.filter(nombre=nombre, empresa=empresa)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                'Ya existe un área con ese nombre en esta empresa.'
            )
        return data


class EquipoSerializer(serializers.ModelSerializer):
    tipo_equipo_nombre = serializers.CharField(source='tipo_equipo.nombre', read_only=True)
    area_nombre = serializers.CharField(source='area.nombre', read_only=True)

    class Meta:
        model = Equipo
        fields = [
            'id', 'codigo', 'nombre', 'tipo_equipo', 'tipo_equipo_nombre',
            'area', 'area_nombre', 'marca', 'modelo', 'numero_serie',
            'fecha_adquisicion', 'activo',
        ]

    def validate_codigo(self, value):
        """Validación de campo: código no puede empezar con espacios ni ser menor a 3."""
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                'El código debe tener al menos 3 caracteres.'
            )
        return value


class OrdenTrabajoSerializer(serializers.ModelSerializer):
    equipo_codigo = serializers.CharField(source='equipo.codigo', read_only=True)
    estado_nombre = serializers.CharField(source='estado.nombre', read_only=True)
    propietario_username = serializers.CharField(
        source='propietario.username', read_only=True
    )

    class Meta:
        model = OrdenTrabajo
        fields = [
            'id', 'numero_orden', 'propietario', 'propietario_username',
            'equipo', 'equipo_codigo', 'estado', 'estado_nombre',
            'descripcion', 'prioridad', 'fecha_inicio', 'fecha_termino',
            'responsable', 'observaciones',
        ]

    def validate_fecha_termino(self, value):
        """Validación de campo: fecha_termino no puede ser anterior a fecha_inicio."""
        fecha_inicio = self.initial_data.get('fecha_inicio')
        if value and fecha_inicio and str(value) < str(fecha_inicio):
            raise serializers.ValidationError(
                'La fecha de término no puede ser anterior a la fecha de inicio.'
            )
        return value


# ─────────────────────────────────────────────────────────────
# Serializers — modelos operacionales
# ─────────────────────────────────────────────────────────────

class EstadoOrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoOrden
        fields = ['id', 'nombre', 'descripcion']


class DetalleOrdenSerializer(serializers.ModelSerializer):
    orden_numero = serializers.CharField(source='orden.numero_orden', read_only=True)

    class Meta:
        model = DetalleOrden
        fields = [
            'id', 'orden', 'orden_numero', 'actividad',
            'horas_trabajo', 'observacion',
        ]

    def validate_horas_trabajo(self, value):
        """Validación de campo: horas_trabajo debe ser > 0."""
        if value <= 0:
            raise serializers.ValidationError(
                'Las horas de trabajo deben ser mayores a 0.'
            )
        return value


class TipoEquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEquipo
        fields = ['id', 'nombre', 'descripcion', 'activo']