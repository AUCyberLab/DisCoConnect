from example import example_diagram1
from discoconnect.computation import get_dominant_morphisms, get_all_morphism_compositions, get_minimal_cut


def main():
    hc = example_diagram1()
    report_diagram(hc)
    hc.draw()
    
    print(get_dominant_morphisms(hc))
    print(get_all_morphism_compositions(hc))
    print(get_minimal_cut(hc))
    
def report_diagram(hc):
    print(f'Domain: {[o.name for o in hc.dom]}')
    print(f'Codomain: {[o.name for o in hc.cod]}')
    print(f'Boxes: {hc.boxes}')


if __name__ == '__main__':
    main()
