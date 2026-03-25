from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont


Point = Tuple[int, int]
Rect = Tuple[int, int, int, int]

ROOT = Path(__file__).resolve().parents[2]
ICON_BASE = ROOT / "docs" / "assets" / "aws-icons" / "minimal"
OUT_MAIN = ROOT / "docs" / "ARCHITECTURE_DIAGRAM_AWS_LOGO.png"
OUT_V3 = ROOT / "docs" / "ARCHITECTURE_DIAGRAM_AWS_LOGO_v3.png"


def load_font(size: int, bold: bool = False):
    names = (
        ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf", "DejaVuSans-Bold.ttf"]
        if bold
        else ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf", "DejaVuSans.ttf"]
    )
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def icon(path: str) -> Path:
    p = ICON_BASE / path
    if not p.exists():
        raise FileNotFoundError(f"Missing icon: {p}")
    return p


ICONS = {
    "internet": icon("internet.png"),
    "user": icon("user.png"),
    "vpc": icon("vpc.png"),
    "igw": icon("igw.png"),
    "nat": icon("nat.png"),
    "alb": icon("alb.png"),
    "eks": icon("eks.png"),
    "ec2": icon("ec2.png"),
    "ssm": icon("ssm.png"),
    "public_subnet": icon("public_subnet.png"),
    "private_subnet": icon("private_subnet.png"),
}


COL = {
    "bg": (248, 251, 255),
    "panel_l": (229, 239, 252),
    "panel_r": (232, 247, 236),
    "vpc": (255, 255, 255),
    "public": (255, 246, 225),
    "private": (236, 244, 253),
    "border": (83, 103, 123),
    "text": (24, 38, 56),
    "sub": (82, 96, 113),
    "app": (34, 84, 147),
    "ops": (79, 92, 109),
    "box": (247, 249, 252),
}


def t_center(draw: ImageDraw.ImageDraw, p: Point, text: str, font, fill=COL["text"]):
    box = draw.multiline_textbbox((0, 0), text, font=font, align="center")
    w, h = box[2] - box[0], box[3] - box[1]
    draw.multiline_text((p[0] - w // 2, p[1] - h // 2), text, font=font, fill=fill, align="center")


def t_left(draw: ImageDraw.ImageDraw, p: Point, text: str, font, fill=COL["text"]):
    draw.multiline_text(p, text, font=font, fill=fill, align="left")


def paste_icon(img: Image.Image, key: str, center: Point, size: int):
    im = Image.open(ICONS[key]).convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)
    img.alpha_composite(im, (center[0] - size // 2, center[1] - size // 2))


def icon_node(img: Image.Image, draw: ImageDraw.ImageDraw, key: str, center: Point, label: str, font, size: int = 62):
    paste_icon(img, key, center, size)
    t_center(draw, (center[0], center[1] + size // 2 + 28), label, font, fill=COL["text"])


def rounded(draw: ImageDraw.ImageDraw, r: Rect, fill, width: int = 2):
    draw.rounded_rectangle(r, radius=14, fill=fill, outline=COL["border"], width=width)


def dashed_line(draw: ImageDraw.ImageDraw, p1: Point, p2: Point, color, width=4, seg=12, gap=8):
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:
        step = seg + gap
        s = 1 if y2 > y1 else -1
        y = y1
        while (y - y2) * s < 0:
            ny = y + s * seg
            if (ny - y2) * s > 0:
                ny = y2
            draw.line((x1, y, x2, ny), fill=color, width=width)
            y += s * step
    elif y1 == y2:
        step = seg + gap
        s = 1 if x2 > x1 else -1
        x = x1
        while (x - x2) * s < 0:
            nx = x + s * seg
            if (nx - x2) * s > 0:
                nx = x2
            draw.line((x, y1, nx, y2), fill=color, width=width)
            x += s * step
    else:
        draw.line((x1, y1, x2, y2), fill=color, width=width)


def arrow_head(draw: ImageDraw.ImageDraw, prev: Point, end: Point, color):
    px, py = prev
    ex, ey = end
    a, b = 10, 6
    if ex == px:
        d = 1 if ey > py else -1
        pts = [(ex, ey), (ex - b, ey - d * a), (ex + b, ey - d * a)]
    else:
        d = 1 if ex > px else -1
        pts = [(ex, ey), (ex - d * a, ey - b), (ex - d * a, ey + b)]
    draw.polygon(pts, fill=color)


def route(draw: ImageDraw.ImageDraw, pts: List[Point], color, dashed=False, width=4):
    for i in range(len(pts) - 1):
        if dashed:
            dashed_line(draw, pts[i], pts[i + 1], color=color, width=width)
        else:
            draw.line((*pts[i], *pts[i + 1]), fill=color, width=width)
    arrow_head(draw, pts[-2], pts[-1], color=color)


def center(r: Rect) -> Point:
    return ((r[0] + r[2]) // 2, (r[1] + r[3]) // 2)


def main():
    W, H = 2600, 1520
    img = Image.new("RGBA", (W, H), COL["bg"] + (255,))
    d = ImageDraw.Draw(img)

    f_title = load_font(44, True)
    f_panel = load_font(28, True)
    f_text = load_font(20, False)
    f_small = load_font(17, False)

    t_center(d, (W // 2, 42), "AWS Architecture: Private App vs Public App with Private EKS", f_title)

    left: Rect = (70, 96, 1260, 1280)
    right: Rect = (1340, 96, 2530, 1280)
    rounded(d, left, COL["panel_l"], 3)
    rounded(d, right, COL["panel_r"], 3)
    t_center(d, (center(left)[0], left[1] + 30), "A) Current Assignment (Private App Access)", f_panel)
    t_center(d, (center(right)[0], right[1] + 30), "B) Org Pattern (Public URL + Private EKS)", f_panel)

    def base(panel: Rect):
        px0, py0, px1, py1 = panel
        vpc = (px0 + 22, py0 + 58, px1 - 22, py1 - 86)
        rounded(d, vpc, COL["vpc"])
        paste_icon(img, "vpc", (vpc[0] + 24, vpc[1] + 24), 34)
        t_left(d, (vpc[0] + 44, vpc[1] + 12), "VPC", f_small, COL["sub"])

        pub = (vpc[0] + 14, vpc[1] + 50, vpc[2] - 14, vpc[1] + 254)
        priv = (vpc[0] + 14, vpc[1] + 282, vpc[2] - 14, vpc[3] - 14)
        rounded(d, pub, COL["public"])
        rounded(d, priv, COL["private"])
        paste_icon(img, "public_subnet", (pub[0] + 14, pub[1] + 14), 24)
        paste_icon(img, "private_subnet", (priv[0] + 14, priv[1] + 14), 24)
        t_left(d, (pub[0] + 28, pub[1] + 6), "Public Subnet", f_small, COL["sub"])
        t_left(d, (priv[0] + 28, priv[1] + 6), "Private Subnet", f_small, COL["sub"])
        return pub, priv

    lpub, lpriv = base(left)
    rpub, rpriv = base(right)

    # Left
    l_admin = (left[0] - 28, 280)
    l_ssm = (left[0] - 4, 360)
    icon_node(img, d, "user", l_admin, "Admin", f_small, 50)
    icon_node(img, d, "ssm", l_ssm, "SSM", f_small, 50)

    l_igw = (lpub[0] + 180, lpub[1] + 126)
    l_nat = (lpub[0] + 420, lpub[1] + 126)
    icon_node(img, d, "igw", l_igw, "Internet Gateway", f_small, 62)
    icon_node(img, d, "nat", l_nat, "NAT Gateway", f_small, 62)

    l_eks = (lpriv[0] + 165, lpriv[1] + 130)
    l_nodes = (lpriv[0] + 420, lpriv[1] + 130)
    icon_node(img, d, "eks", l_eks, "EKS API\n(private endpoint)", f_small, 70)
    icon_node(img, d, "ec2", l_nodes, "EC2 Worker\nNodes", f_small, 62)

    l_ha = (lpriv[0] + 560, lpriv[1] + 95, lpriv[0] + 760, lpriv[1] + 190)
    l_tc = (lpriv[0] + 805, lpriv[1] + 95, lpriv[0] + 1005, lpriv[1] + 190)
    rounded(d, l_ha, COL["box"])
    rounded(d, l_tc, COL["box"])
    t_center(d, center(l_ha), "HAProxy\nService", f_text)
    t_center(d, center(l_tc), "Tomcat\nService", f_text)

    route(
        d,
        [
            (l_admin[0] + 20, l_admin[1] + 8),
            (lpub[0] + 120, l_admin[1] + 8),
            (lpub[0] + 120, center(l_ha)[1]),
            (l_ha[0], center(l_ha)[1]),
        ],
        color=COL["app"],
    )
    route(d, [(l_ha[2], center(l_ha)[1]), (l_tc[0], center(l_tc)[1])], color=COL["app"])
    route(
        d,
        [(l_ssm[0] + 20, l_ssm[1]), (l_eks[0] - 40, l_ssm[1]), (l_eks[0] - 40, l_eks[1] - 10)],
        color=COL["ops"],
        dashed=True,
    )
    route(
        d,
        [
            (l_nodes[0] + 16, l_nodes[1] - 6),
            (l_nodes[0] + 16, lpub[1] + 156),
            (l_nat[0], lpub[1] + 156),
        ],
        color=COL["app"],
    )
    route(d, [(l_nat[0] - 36, l_nat[1]), (l_igw[0] + 36, l_igw[1])], color=COL["app"])

    # Right
    r_users = (right[0] - 10, 275)
    icon_node(img, d, "internet", r_users, "Internet Users", f_small, 56)

    r_igw = (rpub[0] + 130, rpub[1] + 126)
    r_alb = (rpub[0] + 360, rpub[1] + 126)
    r_nat = (rpub[0] + 590, rpub[1] + 126)
    icon_node(img, d, "igw", r_igw, "Internet Gateway", f_small, 62)
    icon_node(img, d, "alb", r_alb, "Public ALB", f_small, 62)
    icon_node(img, d, "nat", r_nat, "NAT Gateway", f_small, 62)

    r_eks = (rpriv[0] + 165, rpriv[1] + 130)
    r_nodes = (rpriv[0] + 410, rpriv[1] + 130)
    icon_node(img, d, "eks", r_eks, "EKS API\n(private endpoint)", f_small, 70)
    icon_node(img, d, "ec2", r_nodes, "EC2 Worker\nNodes", f_small, 62)

    r_ha = (rpriv[0] + 545, rpriv[1] + 95, rpriv[0] + 745, rpriv[1] + 190)
    r_tc = (rpriv[0] + 790, rpriv[1] + 95, rpriv[0] + 990, rpriv[1] + 190)
    rounded(d, r_ha, COL["box"])
    rounded(d, r_tc, COL["box"])
    t_center(d, center(r_ha), "HAProxy\nService", f_text)
    t_center(d, center(r_tc), "Tomcat\nService", f_text)

    route(d, [(r_users[0] + 26, r_users[1]), (r_igw[0] - 36, r_igw[1])], color=COL["app"])
    route(d, [(r_igw[0] + 36, r_igw[1]), (r_alb[0] - 36, r_alb[1])], color=COL["app"])
    route(
        d,
        [(r_alb[0], r_alb[1] + 36), (r_alb[0], r_nodes[1] - 34), (r_nodes[0], r_nodes[1] - 34)],
        color=COL["app"],
    )
    route(d, [(r_nodes[0] + 20, r_nodes[1]), (r_ha[0], center(r_ha)[1])], color=COL["app"])
    route(d, [(r_ha[2], center(r_ha)[1]), (r_tc[0], center(r_tc)[1])], color=COL["app"])
    route(d, [(r_nodes[0] + 16, r_nodes[1] - 6), (r_nat[0], r_nat[1] + 34)], color=COL["app"])
    route(d, [(r_nat[0] - 36, r_nat[1]), (r_igw[0] + 36, r_igw[1])], color=COL["app"])
    route(
        d,
        [(r_alb[0] + 20, r_alb[1] + 20), (r_alb[0] + 130, r_alb[1] + 20), (r_alb[0] + 130, r_nodes[1] - 10), (r_nodes[0] + 34, r_nodes[1] - 10)],
        color=COL["ops"],
        dashed=True,
    )

    # Legend
    leg = (180, 1320, 2420, 1460)
    rounded(d, leg, (255, 255, 255))
    t_left(d, (leg[0] + 18, leg[1] + 14), "Legend", f_text)
    route(d, [(leg[0] + 20, leg[1] + 64), (leg[0] + 130, leg[1] + 64)], color=COL["app"])
    t_left(d, (leg[0] + 150, leg[1] + 50), "Solid blue arrow: application traffic path", f_small, COL["sub"])
    route(d, [(leg[0] + 20, leg[1] + 104), (leg[0] + 130, leg[1] + 104)], color=COL["ops"], dashed=True)
    t_left(d, (leg[0] + 150, leg[1] + 90), "Dashed gray arrow: admin/control/health-check path", f_small, COL["sub"])

    OUT_MAIN.parent.mkdir(parents=True, exist_ok=True)
    rgb = img.convert("RGB")
    rgb.save(OUT_MAIN, format="PNG", optimize=True)
    rgb.save(OUT_V3, format="PNG", optimize=True)
    print(f"Generated {OUT_MAIN}")
    print(f"Generated {OUT_V3}")


if __name__ == "__main__":
    main()
