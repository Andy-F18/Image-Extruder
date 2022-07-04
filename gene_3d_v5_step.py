from PIL import Image


class Face:
    class Vertex:
        def set_vertex_1(self, x, y, z):
            self.v1 = [x, y, z]

        def set_vertex_2(self, x, y, z):
            self.v2 = [x, y, z]

        def set_vertex_3(self, x, y, z):
            self.v3 = [x, y, z]

        def p_vertex1(self):
            return str(self.v1[0]) + ' ' + str(self.v1[1]) + ' ' + str(self.v1[2])

        def p_vertex2(self):
            return str(self.v2[0]) + ' ' + str(self.v2[1]) + ' ' + str(self.v2[2])

        def p_vertex3(self):
            return str(self.v3[0]) + ' ' + str(self.v3[1]) + ' ' + str(self.v3[2])

    def __init__(self):
        self.norm = [0, 0, 0]

    def set_normal(self, x, y, z):
        self.norm = [x, y, z]

    def p_norm(self):
        return str(self.norm[0]) + ' ' + str(self.norm[1]) + ' ' + str(self.norm[2])


class Cube:
    def __init__(self):
        self.name = None

    def set_name(self, name):
        self.name = name


def open_file_W(file, content, bare, bare_label):
    s = 0
    t = len(content)
    n = 0
    with open(file, 'w') as f:
        for i in content:
            f.write("\n" + i)
            s += 1
            l = int(100 * s / t)
            if l != n:
                n = l
                bare['value'] = n
                bare_label.configure(text="Saving : " + str(n) + "%")
                bare.update_idletasks()
                # print('\rsaving... [{} %] '.format(l), end="")


def generate(in_file, out_file, offset, gain, COLOR_SELECT, level, lvl, bare, bare_label, s_RGB):
    f_r = s_RGB[0]
    f_g = s_RGB[1]
    f_b = s_RGB[2]
    tolerance = s_RGB[3]

    new = 0

    img = Image.open(in_file)

    size = img.size
    l = size[0]
    w = size[1]

    pixel = img.load()

    a = 0
    t = l * w

    stl_txt = []

    solid = Cube()
    # solid.set_name('cube1')
    stl_txt.append('solid ' + "cubes")

    for i in range(0, l):
        for j in range(0, w):
            solid.set_name('cube_[' + str(i) + '|' + str(j) + ']')

            pix = pixel[i, j]

            R = pix[0]
            G = pix[1]
            B = pix[2]

            m = (R + G + B) / (3 * 255)

            if level:
                h = calc_h(pix, lvl, s_RGB)
            else:
                h = (m * gain + 1)

            # SELEC_R = (R <= (f_r + tolerance)) and (R >= (f_r - tolerance))
            # SELEC_G = (G <= (f_g + tolerance)) and (G >= (f_g - tolerance))
            # SELEC_B = (B <= (f_b + tolerance)) and (f_b >= (B - tolerance))
            #
            # SELEC = SELEC_R and SELEC_G and SELEC_B

            if not COLOR_SELECT:
                if m >= offset:
                    stl_txt += print_solid(solid, j, i, 0, h)

            # elif COLOR_SELECT:
            #     if (m >= offset) and (SELEC == True):
            #         stl_txt += print_solid(solid, j, i, 0, h)

            elif COLOR_SELECT:
                if m >= offset:
                    stl_txt += print_solid(solid, j, i, 0, h)

            a += 1
            p = int(a / t * 100)
            if p != new:
                new = p
                bare['value'] = new
                bare_label.configure(text="Calcul : " + str(new) + "%")
                bare.update_idletasks()
                # print('\rprocessing... [{} %] '.format(new), end="")

    # print('\nend process')
    # print('------------------------------------------------------')
    stl_txt.append('endsolid')

    file = out_file + '.stl'

    open_file_W('stl_projects/' + file, stl_txt, bare, bare_label)

    # print('\nEnd')


def create_faces(x, y, z, h):
    face = Face()
    ve = face.Vertex

    # bottom face (1)
    ve.set_vertex_1(ve, (x + 0), (y + 0), (z + 0 * h))
    ve.set_vertex_2(ve, (x + 1), (y + 0), (z + 0 * h))
    ve.set_vertex_3(ve, (x + 0), (y + 1), (z + 0 * h))

    face.set_normal(0, 0, 1)

    face_txt = print_facet(face)

    # bottom face (2)
    ve.set_vertex_1(ve, (x + 1), (y + 1), (z + 0 * h))
    ve.set_vertex_2(ve, (x + 0), (y + 1), (z + 0 * h))
    ve.set_vertex_3(ve, (x + 1), (y + 0), (z + 0 * h))

    face.set_normal(0, 0, 1)

    face_txt += print_facet(face)

    # side face y = 0 (1)
    ve.set_vertex_1(ve, (x + 0), (y + 0), (z + 0 * h))
    ve.set_vertex_2(ve, (x + 1), (y + 0), (z + 0 * h))
    ve.set_vertex_3(ve, (x + 1), (y + 0), (z + 1 * h))

    face.set_normal(0, 1, 0)

    face_txt += print_facet(face)

    # side face y = 0 (2)
    ve.set_vertex_1(ve, (x + 0), (y + 0), (z + 0 * h))
    ve.set_vertex_2(ve, (x + 1), (y + 0), (z + 1 * h))
    ve.set_vertex_3(ve, (x + 0), (y + 0), (z + 1 * h))

    face.set_normal(0, 1, 0)

    face_txt += print_facet(face)

    # side face x = 0 (1)
    ve.set_vertex_1(ve, (x + 0), (y + 0), (z + 0 * h))
    ve.set_vertex_2(ve, (x + 0), (y + 1), (z + 0 * h))
    ve.set_vertex_3(ve, (x + 0), (y + 1), (z + 1 * h))

    face.set_normal(1, 0, 0)

    face_txt += print_facet(face)

    # side face x = 0 (2)
    ve.set_vertex_1(ve, (x + 0), (y + 0), (z + 0 * h))
    ve.set_vertex_2(ve, (x + 0), (y + 1), (z + 1 * h))
    ve.set_vertex_3(ve, (x + 0), (y + 0), (z + 1 * h))

    face.set_normal(1, 0, 0)

    face_txt += print_facet(face)

    # side face y = 1 (1)
    ve.set_vertex_1(ve, (x + 1), (y + 1), (z + 0 * h))
    ve.set_vertex_2(ve, (x + 0), (y + 1), (z + 0 * h))
    ve.set_vertex_3(ve, (x + 0), (y + 1), (z + 1 * h))

    face.set_normal(0, 1, 0)

    face_txt += print_facet(face)

    # side face y = 1 (2)
    ve.set_vertex_1(ve, (x + 1), (y + 1), (z + 0 * h))
    ve.set_vertex_2(ve, (x + 0), (y + 1), (z + 1 * h))
    ve.set_vertex_3(ve, (x + 1), (y + 1), (z + 1 * h))

    face.set_normal(0, 1, 0)

    face_txt += print_facet(face)

    # side face x = 1 (1)
    ve.set_vertex_1(ve, (x + 1), (y + 0), (z + 0 * h))
    ve.set_vertex_2(ve, (x + 1), (y + 1), (z + 0 * h))
    ve.set_vertex_3(ve, (x + 1), (y + 1), (z + 1 * h))

    face.set_normal(1, 0, 0)

    face_txt += print_facet(face)

    # side face x = 1 (2)
    ve.set_vertex_1(ve, (x + 1), (y + 0), (z + 0 * h))
    ve.set_vertex_2(ve, (x + 1), (y + 1), (z + 1 * h))
    ve.set_vertex_3(ve, (x + 1), (y + 0), (z + 1 * h))

    face.set_normal(1, 0, 0)

    face_txt += print_facet(face)

    # bottom face (1)
    ve.set_vertex_1(ve, (x + 0), (y + 0), (z + 1 * h))
    ve.set_vertex_2(ve, (x + 1), (y + 0), (z + 1 * h))
    ve.set_vertex_3(ve, (x + 0), (y + 1), (z + 1 * h))

    face.set_normal(0, 0, 1)

    face_txt += print_facet(face)

    # bottom face (2)
    ve.set_vertex_1(ve, (x + 1), (y + 1), (z + 1 * h))
    ve.set_vertex_2(ve, (x + 0), (y + 1), (z + 1 * h))
    ve.set_vertex_3(ve, (x + 1), (y + 0), (z + 1 * h))

    face.set_normal(0, 0, 1)

    face_txt += print_facet(face)

    return face_txt


def calc_h(pix, levels, s_RGBs):
    R = pix[0]
    G = pix[1]
    B = pix[2]

    f_rs = s_RGBs[0]
    f_gs = s_RGBs[1]
    f_bs = s_RGBs[2]
    tolerance = s_RGBs[3]

    c = 0
    SELEC = False

    while c < len(f_rs) and not SELEC:
        f_r = f_rs[c]
        f_g = f_gs[c]
        f_b = f_bs[c]
        level = levels[c]

        c += 1

        SELEC_R = (R <= (f_r + tolerance)) and (R >= (f_r - tolerance))
        SELEC_G = (G <= (f_g + tolerance)) and (G >= (f_g - tolerance))
        SELEC_B = (B <= (f_b + tolerance)) and (f_b >= (B - tolerance))

        SELEC = SELEC_R and SELEC_G and SELEC_B

    if not SELEC:
        level = 0

    return level


def print_solid(solid, x, y, z, h):
    solid_txt = []

    name = solid.name

    # solid_txt.append('solid ' + name)

    solid_txt += create_faces(x, y, z, h)

    # solid_txt.append('endsolid')

    # for t in solid_txt:
    #     print(t)

    # open_file_W(file, solid_txt)
    return solid_txt


def print_facet(f):
    face_text = []

    normal = f.p_norm()

    vertex = f.Vertex
    v1 = vertex.p_vertex1(vertex)
    v2 = vertex.p_vertex2(vertex)
    v3 = vertex.p_vertex3(vertex)

    face_text.append(' facet normal ' + normal)
    face_text.append('  outer loop')
    face_text.append('   vertex ' + v1)
    face_text.append('   vertex ' + v2)
    face_text.append('   vertex ' + v3)
    face_text.append('  endloop')
    face_text.append(' endfacet')

    return face_text


if __name__ == '__main__':
    generate()
