from OpenGL.GL import glGetString, GL_VERSION, GL_SHADING_LANGUAGE_VERSION

def get_opengl_info():
    version = glGetString(GL_VERSION).decode('utf-8')
    glsl_version = glGetString(GL_SHADING_LANGUAGE_VERSION).decode('utf-8')
    return version, glsl_version

if __name__ == "__main__":
    opengl_version, glsl_version = get_opengl_info()
    print("OpenGL Version:", opengl_version)
    print("GLSL Version:", glsl_version)