import gimpfu
import os
import os.path
import sys
import toml

import logging

TOML_EXT = '.toml'

logger = logging.getLogger(__name__)


def process(path):
    print('process')
    results = []

    if os.path.isfile(path):
        base, ext = os.path.splitext(path)
        print((base, ext))
        if ext != '.xcf':
            # May wish to raise an exception
            return None

        if not os.path.isfile(base + TOML_EXT):
            logger.warn('No build sidecar found for {}!'.format(path))
            return None

        return [handle(path, base + TOML_EXT)]
    elif os.path.isdir(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in [filename for filename in filenames if os.path.splitext(filename)[1] == '.xcf']:

                results += process(os.path.join(dirpath, filename)) or []

    return results


def handle(gimp_filepath, sidecar_filepath):

    image = gimpfu.pdb.gimp_file_load(
        gimp_filepath,
        os.path.basename(gimp_filepath),
        run_mode=gimpfu.RUN_NONINTERACTIVE
    )

    layer_by_name = dict((layer.name, layer) for layer in image.layers)

    if os.path.isfile(sidecar_filepath):
        with open(sidecar_filepath, 'r') as fh:
            config = toml.load(fh)

    else:
        # ToDo may want to include some sort of per-directory defaults,
        # not sure how
        raise

    for target, target_conf in config.items():

        export_image = gimpfu.pdb.gimp_image_duplicate(image)
        for layer in export_image.layers:
            print((layer, layer.name, layer.parent, layer.children))
            print(target_conf)
            if layer.name in target_conf.get('enabled_layers', []):
                print('making {} visible'.format(layer.name))
                layer.visible = True
                continue
                gimpfu.pdb.gimp_image_delete(export_image)
            layer.visible = False

        export_layer = gimpfu.pdb.gimp_image_merge_visible_layers(export_image, gimpfu.CLIP_TO_IMAGE)
        print('el')
        print(export_image.layers)
        gimpfu.pdb.file_png_save(
            export_image, export_layer, target,
            os.path.basename(target), 0, 9, 1, 1, 1, 1, 1)
        gimpfu.pdb.gimp_image_delete(export_image)


def main():
    if len(sys.argv) > 1:
        for fp in sys.argv[1:]:
            process(fp)
    else:
        process(os.getcwd())


class NoSidecar(object):
    pass

if __name__ == '__main__':
    main()
