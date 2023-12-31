from pygame.font import get_fonts

def is_char(arg):
    return len(arg) == 1 and isinstance(arg, str)

def is_str(arg):
    return len(arg) > 1 and isinstance(arg, str)

def string_insert(string, index, char):
    list_s = list(string)
    list_s.insert(index, char)
    return ''.join(list_s)

def anchor_calculation(parent, child_surface, anchor, offset_x, offset_y):

    try:
        pw, ph = parent.get_size()
    except:
        pw, ph = parent.size

    cw, ch = child_surface.get_size()
    mx, my = offset_x, offset_y

    anchor_dictionary = {
        'topleft': [0+mx, 0+my],
        'topright': [pw-cw+mx, 0+my],
        'bottomleft': [0+mx, ph-ch+my],
        'bottomright': [pw-cw+mx, ph-ch+my],
        'center': [pw//2-cw//2+mx, ph//2-ch//2+my+1],
        'midtop': [pw//2-cw//2+mx, my],
        'midbottom': [pw//2-cw//2+mx, ph-ch+my],
        'midleft': [mx, ph//2-ch//2+my],
        'midright': [pw-cw+mx, ph//2-ch//2+my],
    }

    return anchor_dictionary[anchor]

def ascii(char):
    if len(char): return ord(char)
    return False

def nearest_to(x, y, near_val):
    if abs(x-near_val) < abs(y-near_val):
        return x
    elif abs(x-near_val) == abs(y-near_val):
        return x+y/2
    else:
        return y

