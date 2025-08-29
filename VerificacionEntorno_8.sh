# Verificar que todo está configurado correctamente
echo "=== Verificación del Entorno ==="
echo "Directorio actual: $(pwd)"
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"
echo "Virtual env activo: $VIRTUAL_ENV"
echo ""
echo "Estructura del proyecto:"
tree -L 2 ~/story-enhancer-ai

echo ""
echo "Archivos de configuración:"
ls -la | grep -E "\.(env|gitignore|md|txt)$"