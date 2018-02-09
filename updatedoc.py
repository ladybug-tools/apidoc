import sys
import os
import os.path as path
import codecs
import pdoc


def listdir(path):
    """List all the .py files in folder and subfolders."""
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in [f for f in filenames if f.endswith(".py")]:
            if os.path.splitext(filename)[0] != '__init__':
                yield '"%s"' % os.path.join(
                    dirpath, filename).replace(path, '')[1:-3].replace('\\', '.')


def module_file(m, html_dir):
    mbase = path.join(html_dir, *m.name.split('.'))
    if m.is_package():
        return path.join(mbase, pdoc.html_package_name)
    else:
        return '%s%s' % (mbase, pdoc.html_module_suffix)


def html_out(m, html_dir, html=True):
    f = module_file(m, html_dir)
    if not html:
        f = module_file(m, html_dir).replace(".html", ".md")
    dirpath = path.dirname(f)
    if not os.access(dirpath, os.R_OK):
        os.makedirs(dirpath)
    try:
        with codecs.open(f, 'w+', 'utf-8') as w:
            if not html:
                out = m.text()
            else:
                out = m.html(source=True, top_module='ladybug')
            w.write(out)
            # print(out, file=w)
    except Exception:
        try:
            os.unlink(f)
        except Exception:
            pass
        raise

    for submodule in m.submodules():
        print(submodule.name)
        html_out(submodule, html_dir, html)


if __name__ == '__main__':
    sys.path.append(r'C:\Users\Mostapha\Documents\code\ladybug-tools\ladybug')
    sys.path.append(r'C:\Users\Mostapha\Documents\code\ladybug-tools\honeybee')
    sys.path.append(r'C:\Users\Mostapha\Documents\code\ladybug-tools\butterfly')
    import ladybug
    # from ladybug import *
    import honeybee
    from honeybee import *
    # import butterfly
    # from butterfly import *
    html_dir = r'C:\Users\Mostapha\Documents\code\ladybug-tools\apidoc'
    root = os.path.dirname(honeybee.__file__)
    os.chdir(root)
    # with open(os.path.join(root, '__init__.py'), 'wb') as init:
    #     init.write('__all__ = [%s]' % ','.join(listdir(root)))
    module = pdoc.Module(honeybee, docfilter=None, allsubmodules=True)
    html_out(module, html_dir)
