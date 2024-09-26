## Correr

### Parámetros
- **URL-ORIGEN**  : URL desde donde tomar el token.
- **URL-DESTINO** : URL donde se introducirá el token.
- **NAVEGADOR**   : Navegador en el que se desea introducir el token.
- **PERFIL**      : Perfil del usuario en el navegador.

### Instrucciones
Ejecuta los siguientes comandos en la terminal:

```bash
python3.8 -m pip install -r requirements.txt
python3.8 ./main --URL-ORIGEN <URL-ORIGEN> --URL-DESTINO <URL-DESTINO> --NAVEGADOR <NAVEGADOR> --PERFIL <PERFIL>
```
### Ejemplo

```bash
python3.8 -m pip install -r requirements.txt
python3.8 ./main --URL-ORIGEN https://buenclub-frontend.stg.sportclub.com.ar/socios --URL-DESTINO https://buenclub-frontend.dev.sportclub.com.ar/socios --NAVEGADOR brave --PERFIL 6nmikg7p.default-release
```
