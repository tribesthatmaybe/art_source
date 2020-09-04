import collections
import gimpfu
import logging
import os
import os.path
import six
import sys
import toml

if six.PY3:
    import abc.abc as abc

else:
    import collections as abc

TOML_EXT = '.toml'
ALL_LAYERS = 'all'

logger = logging.getLogger(__name__)


def process(path):
    results = []

    if os.path.isfile(path):
        base, ext = os.path.splitext(path)
        if ext != '.xcf':
            # May wish to raise an exception
            return None

        if not os.path.isfile(base + TOML_EXT):
            logger.warn('No build sidecar found for {}!'.format(path))
            return None

        return [handle(path, base + TOML_EXT)]
    elif os.path.isdir(path):

        for dirpath, dirnames, filenames in os.walk(path):

            for filename in [filename for filename in filenames
                             if os.path.splitext(filename)[1] == '.xcf']:

                results += process(os.path.join(dirpath, filename)) or []

    return results


def _is_collection(item):
    # Python2 doesn't have collection (sized, iterable container)
    # Never treat strings as collections even though they are
    if isinstance(item, basestring):
        return False
    if six.PY3 and isinstance(item, collections.Collection):
        return True
    elif six.PY2 and isinstance(item, collections.Iterable) and isinstance(item, collections.Container) and isinstance(item, collections.Sized):
        return True
    return False


def _merge(v1, v2):
    """
    Do a deep merge of two dictionaries.
    If this encounters a hash or a collection, it will handle the values by
    merging them (preferring d2's values when there are two values at the same
    key).

    Args:
        d1 (dict): The base dictionary into which to merge another dictionary
        d2 (dict): The dictionary to merge into d1, overwriting values that
                   conflict

    """

    if six.PY2:
        handled_abcs = (abc.Mapping,)
    else:
        handled_abcs = (abc.Mapping, abc.Collection)


    # Avoiding sequence/collection steps below
    if isinstance(v2, basestring):
        return v2

    if isinstance(v1, abc.Mapping) and isinstance(v2, abc.Mapping):
        res = {}
        for k in set(v1.keys()) | set(v2.keys()):
            if k not in v2:
                res[k] = v1[k]
            elif k not in v1:
                res[k] = v2[k]
            else:
                kr = _merge(v1[k], v2[k])
                res[k] = kr
        return res

    # Possible it could be a non-sequential collection, in which case comparing
    # this way would be nonsensical
    elif isinstance(v1, abc.Sequence) and isinstance(v2, abc.Sequence) and not isinstance(v1, basestring):
        res = list(v1)
        for idx, element in enumerate(v2):
            if idx >= len(res):
                res.append(element)
            elif isinstance(element, handled_abcs) or _is_collection(element):
                res[idx] = _merge(v1[idx], v2[idx])
            else:
                # non-merged type, add to list
                if element not in res:
                    res.append(element)
        return res

    elif _is_collection(v1) and _is_collection(v2):
        return list(v1) + [el for el in v2 if el not in v1]

    # Neither a mapping nor a collection, just use v2
    return v2


def handle(gimp_filepath, sidecar_filepath):
    """
    Handle building maps from a single gimp file
    """

    image = gimpfu.pdb.gimp_file_load(
        gimp_filepath,
        os.path.basename(gimp_filepath),
        run_mode=gimpfu.RUN_NONINTERACTIVE
    )

    if os.path.isfile(sidecar_filepath):
        with open(sidecar_filepath, 'r') as fh:
            config = toml.load(fh)

    else:
        # ToDo may want to include some sort of per-directory defaults,
        # not sure which way I'd want to do that.
        raise NoSidecar("Sidecar file {} does not exist!".format(sidecar_filepath))

    all_layers = config.pop(ALL_LAYERS)

    for target, target_conf in config.items():
        target_conf = _merge(all_layers, target_conf)
        export_image = gimpfu.pdb.gimp_image_duplicate(image)
        for layer in export_image.layers:
            if layer.name in target_conf.get('enabled_layers', []):
                layer.visible = True
                continue
                gimpfu.pdb.gimp_image_delete(export_image)
            layer.visible = False

        export_layer = gimpfu.pdb.gimp_image_merge_visible_layers(export_image, gimpfu.CLIP_TO_IMAGE)
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
