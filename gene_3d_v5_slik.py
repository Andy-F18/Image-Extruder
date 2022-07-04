from PIL import Image
import numpy as np


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
            if (l != n):
                n = l
                bare['value'] = n
                bare_label.configure(text="Saving : " + str(n) + "%")
                bare.update_idletasks()
                # print('\rsaving... [{} %] '.format(l), end="")


def generate(in_file, out_file, offset, gain, COLOR_SELECT, level, lvl, bare, bare_label, s_RGB):
    res = 0
    new = 0

    # img = Image.open(in_file)
    img = Image.open(in_file)

    size = img.size
    w = size[0]
    h = size[1]

    pixel = img.load()

    a = 0
    t = (h - 1) * (w - 1)

    stl_txt = []
    stl_txt.append('solid 1')

    solid = Cube()

    for i in range(0, h-1):
        for j in range(0, w-1):
            p00 = calc_pix(pixel[j, i])
            p01 = calc_pix(pixel[j + 1, i])
            p11 = calc_pix(pixel[j + 1, i + 1])
            p10 = calc_pix(pixel[j, i + 1])

            if COLOR_SELECT:
                if level:
                    m00 = calc_h(pixel[j, i], lvl, s_RGB)
                    m01 = calc_h(pixel[j + 1, i], lvl, s_RGB)
                    m11 = calc_h(pixel[j + 1, i + 1], lvl, s_RGB)
                    m10 = calc_h(pixel[j, i + 1], lvl, s_RGB)
                else:
                    niv = np.sqrt(pixel[j, i][0]**2 + pixel[j, i][1]**2 + pixel[j, i][2]**2)
                    m00 = calc_h(pixel[j, i], niv, s_RGB)
                    m01 = calc_h(pixel[j + 1, i], niv, s_RGB)
                    m11 = calc_h(pixel[j + 1, i + 1], niv, s_RGB)
                    m10 = calc_h(pixel[j, i + 1], niv, s_RGB)
            else:
                m00 = p00 * gain
                m01 = p01 * gain
                m11 = p11 * gain
                m10 = p10 * gain

            n1 = calc_normal(m00, m01, m10)
            n2 = calc_normal(m11, m10, m01)

            if (p00 > offset) or (p01 > offset) or (p10 > offset):
                pt1 = [j, i, m00]
                pt2 = [j + 1, i, m01]
                pt3 = [j, i + 1, m10]
                stl_txt += create_face(pt1, pt2, pt3, n1)

                pt1 = [j, i, 0]
                pt2 = [j + 1, i, 0]
                pt3 = [j, i + 1, 0]
                n1 = [0, 0, 1]
                stl_txt += create_face(pt1, pt2, pt3, n1)

            if (p11 > offset) or (p01 > offset) or (p10 > offset):
                pt1 = [j + 1, i + 1, m11]
                pt2 = [j, i + 1, m10]
                pt3 = [j + 1, i, m01]
                stl_txt += create_face(pt1, pt2, pt3, n2)

                pt1 = [j + 1, i + 1, 0]
                pt2 = [j, i + 1, 0]
                pt3 = [j + 1, i, 0]
                n2 = [0, 0, 1]
                stl_txt += create_face(pt1, pt2, pt3, n2)

            a += 1
            p = int(a / t * 100)
            if p != new:
                new = p
                bare['value'] = new
                bare_label.configure(text="Calcul : " + str(new) + "%")
                bare.update_idletasks()
                # print('\rprocessing... [{} %] '.format(new), end="")

    stl_txt.append('endsolid')

    # print('\nend process')
    # print('------------------------------------------------------')

    # file = input('output name : ')
    file = out_file + '.stl'

    open_file_W('stl_projects/' + file, stl_txt, bare, bare_label)

    # print('\nEnd')


def calc_pix(pix):
    R = pix[0]
    G = pix[1]
    B = pix[2]

    m = (R + G + B) / (3 * 255)

    return m


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

        try:
            level = levels[c]
        except IndexError:
            level = levels

        c += 1

        SELEC_R = (R <= (f_r + tolerance)) and (R >= (f_r - tolerance))
        SELEC_G = (G <= (f_g + tolerance)) and (G >= (f_g - tolerance))
        SELEC_B = (B <= (f_b + tolerance)) and (f_b >= (B - tolerance))

        SELEC = SELEC_R and SELEC_G and SELEC_B

    if not SELEC:
        level = 0

    return level


def calc_normal(z1, z2, z3):
    AB = [1, 0, z2 - z1]
    AC = [0, 1, z3 - z1]

    zAB = AB[2]
    zAC = AC[2]

    z = - 1
    x = - z * zAB
    y = - z * zAC

    n = [x, y, z]

    return n


def create_face(p1, p2, p3, n):
    face_text = []

    normal = str(n[0]) + ' ' + str(n[1]) + ' ' + str(n[2])

    p1 = str(p1[0]) + ' ' + str(p1[1]) + ' ' + str(p1[2])
    p2 = str(p2[0]) + ' ' + str(p2[1]) + ' ' + str(p2[2])
    p3 = str(p3[0]) + ' ' + str(p3[1]) + ' ' + str(p3[2])

    face_text.append(' facet normal ' + normal)
    face_text.append('  outer loop')
    face_text.append('   vertex ' + p1)
    face_text.append('   vertex ' + p2)
    face_text.append('   vertex ' + p3)
    face_text.append('  endloop')
    face_text.append(' endfacet')

    return face_text


if __name__ == '__main__':
    generate()