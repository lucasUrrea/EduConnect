# 📊 DIAGRAMA DE FLUJO - SISTEMA DE INICIO DE SESIÓN

## Diagrama de Flujo Principal

```mermaid
flowchart LR
    Start([Usuario accede a /login/]) --> CheckAuth{¿Usuario ya<br/>autenticado?}
    
    CheckAuth -->|Sí| RedirectDashboard[Redirigir según rol]
    CheckAuth -->|No| ShowForm[Mostrar formulario de login]
    
    ShowForm --> UserInput[Usuario ingresa:<br/>- Email<br/>- Password]
    UserInput --> Submit[Usuario presiona<br/>'Iniciar Sesión']
    
    Submit --> ValidateCSRF{¿CSRF Token<br/>válido?}
    ValidateCSRF -->|No| Error403[Error 403<br/>Forbidden]
    ValidateCSRF -->|Sí| AuthDjango{¿Autenticación<br/>Django exitosa?}
    
    AuthDjango -->|Sí| LoadProfile[Cargar perfil<br/>desde Usuarios]
    AuthDjango -->|No| TryCustomAuth[Intentar autenticación<br/>con tabla Usuarios]
    
    TryCustomAuth --> CheckUser{¿Usuario<br/>existe?}
    CheckUser -->|No| ErrorCred1[Mensaje: Credenciales<br/>inválidas]
    CheckUser -->|Sí| CheckPassword{¿Password<br/>correcto?}
    
    CheckPassword -->|No| ErrorCred2[Mensaje: Credenciales<br/>inválidas]
    CheckPassword -->|Sí| CheckActive{¿Usuario<br/>activo?}
    
    CheckActive -->|No| ErrorInactive[Mensaje: Usuario<br/>inactivo]
    CheckActive -->|Sí| CreateDjangoUser[Crear/actualizar<br/>usuario Django]
    
    CreateDjangoUser --> AuthenticateDjango[Autenticar con<br/>Django auth]
    AuthenticateDjango --> LoadProfile
    
    LoadProfile --> SaveSession[Guardar en sesión:<br/>- usuario_id<br/>- tipo_usuario<br/>- nombre_completo]
    
    SaveSession --> CheckStaff{¿Es staff o<br/>superuser?}
    CheckStaff -->|Sí| RedirectAdmin[Redirigir a /admin/]
    CheckStaff -->|No| CheckRole{¿Tipo de<br/>usuario?}
    
    CheckRole -->|estudiante| RedirectStudent[Redirigir a<br/>/dashboard/estudiante/]
    CheckRole -->|docente| RedirectTeacher[Redirigir a<br/>/dashboard/docente/]
    CheckRole -->|Otro| RedirectHome[Redirigir a /home/]
    
    RedirectAdmin --> Middleware1[Middleware:<br/>EnsureUsuarioSession]
    RedirectStudent --> Middleware1
    RedirectTeacher --> Middleware1
    RedirectHome --> Middleware1
    
    Middleware1 --> Middleware2[Middleware:<br/>RateLimitMiddleware]
    Middleware2 --> Middleware3[Middleware:<br/>SecurityHeaders]
    Middleware3 --> Dashboard([Mostrar Dashboard])
    
    ErrorCred1 --> ShowForm
    ErrorCred2 --> ShowForm
    ErrorInactive --> ShowForm
    Error403 --> ShowForm
    
    style Start fill:#e1f5ff
    style Dashboard fill:#c8e6c9
    style RedirectAdmin fill:#fff9c4
    style RedirectStudent fill:#bbdefb
    style RedirectTeacher fill:#c5cae9
    style ErrorCred1 fill:#ffcdd2
    style ErrorCred2 fill:#ffcdd2
    style ErrorInactive fill:#ffcdd2
    style Error403 fill:#ffcdd2
```

## Diagrama de Validación de Permisos (Después del Login)

```mermaid
flowchart TD
    Request([Request a URL]) --> Middleware{Middleware:<br/>RoleBasedAccess}
    
    Middleware --> CheckPublic{¿Es ruta<br/>pública?}
    CheckPublic -->|Sí<br/>/login/, /static/| Allow1[Permitir acceso]
    CheckPublic -->|No| CheckAuth{¿Usuario<br/>autenticado?}
    
    CheckAuth -->|No| Block1[Bloquear<br/>Redirigir a /login/]
    CheckAuth -->|Sí| CheckAdmin{¿Es admin o<br/>superuser?}
    
    CheckAdmin -->|Sí| Allow2[Permitir acceso<br/>total]
    CheckAdmin -->|No| CheckSession{¿tipo_usuario<br/>en sesión?}
    
    CheckSession -->|No| Allow3[Permitir<br/>sesión se establece]
    CheckSession -->|Sí| CheckRoute{¿Tipo de<br/>ruta?}
    
    CheckRoute -->|Estudiante only| ValidateStudent{¿tipo_usuario<br/>= estudiante?}
    CheckRoute -->|Docente only| ValidateTeacher{¿tipo_usuario<br/>= docente?}
    CheckRoute -->|Compartida| Allow4[Permitir acceso]
    
    ValidateStudent -->|Sí| Allow5[Permitir acceso]
    ValidateStudent -->|No| Block2[Bloquear<br/>Mensaje: Exclusivo<br/>para estudiantes]
    
    ValidateTeacher -->|Sí| Allow6[Permitir acceso]
    ValidateTeacher -->|No| Block3[Bloquear<br/>Mensaje: Exclusivo<br/>para docentes]
    
    Allow1 --> View([Mostrar Vista])
    Allow2 --> View
    Allow3 --> View
    Allow4 --> View
    Allow5 --> View
    Allow6 --> View
    
    Block1 --> Log1[Registrar en<br/>LogsActividad]
    Block2 --> Log2[Registrar intento<br/>de acceso denegado]
    Block3 --> Log3[Registrar intento<br/>de acceso denegado]
    
    Log1 --> Redirect1[Redirigir a /login/]
    Log2 --> Redirect2[Redirigir a /home/<br/>con mensaje error]
    Log3 --> Redirect3[Redirigir a /home/<br/>con mensaje error]
    
    style Request fill:#e1f5ff
    style View fill:#c8e6c9
    style Allow1 fill:#c8e6c9
    style Allow2 fill:#c8e6c9
    style Allow3 fill:#c8e6c9
    style Allow4 fill:#c8e6c9
    style Allow5 fill:#c8e6c9
    style Allow6 fill:#c8e6c9
    style Block1 fill:#ffcdd2
    style Block2 fill:#ffcdd2
    style Block3 fill:#ffcdd2
```

## Diagrama de Estados de Usuario

```mermaid
stateDiagram-v2
    [*] --> NoAutenticado: Usuario accede al sistema
    
    NoAutenticado --> FormularioLogin: GET /login/
    FormularioLogin --> ValidandoCredenciales: POST con email/password
    
    ValidandoCredenciales --> ErrorCredenciales: Credenciales inválidas
    ValidandoCredenciales --> Autenticando: Credenciales válidas
    
    ErrorCredenciales --> FormularioLogin: Mostrar mensaje de error
    
    Autenticando --> SesionEstablecida: Autenticación exitosa
    SesionEstablecida --> Estudiante: tipo_usuario = 'estudiante'
    SesionEstablecida --> Docente: tipo_usuario = 'docente'
    SesionEstablecida --> Admin: is_staff = True
    
    Estudiante --> DashboardEstudiante: Redirigir
    Docente --> DashboardDocente: Redirigir
    Admin --> PanelAdmin: Redirigir
    
    DashboardEstudiante --> AccesoRestringido: Intenta acceder a ruta de docente
    DashboardDocente --> AccesoRestringido: Intenta acceder a ruta de estudiante
    
    AccesoRestringido --> DashboardEstudiante: Bloquear y redirigir
    AccesoRestringido --> DashboardDocente: Bloquear y redirigir
    
    DashboardEstudiante --> CerrandoSesion: Logout
    DashboardDocente --> CerrandoSesion: Logout
    PanelAdmin --> CerrandoSesion: Logout
    
    CerrandoSesion --> [*]: Sesión terminada
```

## Diagrama de Secuencia

```mermaid
sequenceDiagram
    actor Usuario
    participant Browser
    participant Django
    participant Middleware
    participant AuthSystem
    participant Database
    participant Session
    
    Usuario->>Browser: Accede a /login/
    Browser->>Django: GET /login/
    Django->>Browser: Mostrar formulario
    
    Usuario->>Browser: Ingresa email y password
    Browser->>Django: POST /login/
    
    Django->>Middleware: Validar CSRF
    Middleware-->>Django: CSRF válido
    
    Django->>AuthSystem: authenticate(email, password)
    AuthSystem->>Database: SELECT * FROM auth_user
    Database-->>AuthSystem: Usuario encontrado/no encontrado
    
    alt Usuario Django existe
        AuthSystem-->>Django: Usuario autenticado
    else Usuario no existe en auth_user
        Django->>Database: SELECT * FROM Usuarios
        Database-->>Django: Usuario personalizado
        Django->>AuthSystem: Crear usuario Django
        AuthSystem->>Database: INSERT INTO auth_user
        Database-->>AuthSystem: Usuario creado
        AuthSystem-->>Django: Usuario autenticado
    end
    
    Django->>Database: SELECT * FROM Usuarios
    Database-->>Django: Datos del perfil
    
    Django->>Session: Guardar usuario_id, tipo_usuario
    Session-->>Django: Sesión establecida
    
    Django->>Django: Determinar redirección según rol
    
    alt Es estudiante
        Django->>Browser: Redirect /dashboard/estudiante/
    else Es docente
        Django->>Browser: Redirect /dashboard/docente/
    else Es admin
        Django->>Browser: Redirect /admin/
    end
    
    Browser->>Django: GET dashboard
    Django->>Middleware: Validar permisos
    Middleware->>Session: Verificar tipo_usuario
    Session-->>Middleware: Rol confirmado
    Middleware-->>Django: Acceso permitido
    
    Django->>Database: Cargar datos del dashboard
    Database-->>Django: Datos
    Django->>Browser: Renderizar dashboard
    Browser->>Usuario: Mostrar dashboard
```

## Diagrama de Componentes del Sistema

```mermaid
graph TB
    subgraph "Cliente"
        Browser[Navegador Web]
    end
    
    subgraph "Capa de Presentación"
        LoginView[login_view]
        DashboardEst[dashboard_estudiante]
        DashboardDoc[dashboard_docente]
    end
    
    subgraph "Middlewares"
        CSRF[CsrfViewMiddleware]
        Auth[AuthenticationMiddleware]
        Session[SessionMiddleware]
        EnsureUser[EnsureUsuarioSessionMiddleware]
        RateLimit[RateLimitMiddleware]
        Security[SecurityHeadersMiddleware]
    end
    
    subgraph "Sistema de Autenticación"
        DjangoAuth[Django Auth System]
        CustomAuth[Custom Auth Logic]
    end
    
    subgraph "Modelos"
        UserModel[auth_user]
        UsuariosModel[Usuarios]
        EstudiantesModel[Estudiantes]
        DocentesModel[Docentes]
        LogsModel[LogsActividad]
    end
    
    subgraph "Base de Datos"
        SQLite[(SQLite DB)]
    end
    
    Browser -->|GET /login/| CSRF
    CSRF --> Session
    Session --> Auth
    Auth --> LoginView
    
    LoginView -->|authenticate| DjangoAuth
    LoginView -->|fallback| CustomAuth
    
    DjangoAuth --> UserModel
    CustomAuth --> UsuariosModel
    
    UsuariosModel --> EstudiantesModel
    UsuariosModel --> DocentesModel
    
    LoginView -->|Redirect| EnsureUser
    EnsureUser --> RateLimit
    RateLimit --> Security
    
    Security -->|estudiante| DashboardEst
    Security -->|docente| DashboardDoc
    
    DashboardEst --> EstudiantesModel
    DashboardDoc --> DocentesModel
    
    UserModel --> SQLite
    UsuariosModel --> SQLite
    EstudiantesModel --> SQLite
    DocentesModel --> SQLite
    LogsModel --> SQLite
    
    RateLimit -.->|log| LogsModel
    Security -.->|log| LogsModel
```

---

## 📝 Descripción de Flujos

### 1. **Flujo Principal de Login**
1. Usuario accede a `/login/`
2. Sistema verifica si ya está autenticado
3. Usuario ingresa credenciales (email + password)
4. Sistema valida CSRF token
5. Intenta autenticación con Django Auth
6. Si falla, intenta con tabla Usuarios personalizada
7. Valida password y estado activo
8. Crea/actualiza usuario Django si es necesario
9. Guarda datos en sesión
10. Redirige según rol (estudiante/docente/admin)

### 2. **Validación de Permisos**
1. Usuario hace request a una URL
2. Middleware verifica si es ruta pública
3. Si no, verifica autenticación
4. Verifica si es admin (acceso total)
5. Verifica tipo de usuario en sesión
6. Valida si la ruta corresponde al rol
7. Permite o bloquea acceso
8. Registra intentos de acceso denegado

### 3. **Roles y Redirecciones**
- **Estudiante** → `/dashboard/estudiante/`
- **Docente** → `/dashboard/docente/`
- **Admin** → `/admin/`

---

## 🎨 Leyenda de Colores

- 🔵 **Azul claro**: Inicio/entrada del flujo
- 🟢 **Verde**: Éxito/acceso permitido
- 🔴 **Rojo**: Error/acceso denegado
- 🟡 **Amarillo**: Admin/casos especiales

---

**Generado el:** 10/11/2025
