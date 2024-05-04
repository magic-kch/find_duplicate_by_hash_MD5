import time


def m_pbar(a):
    percent = 100/a
    progress = 0
    for buf in range(a):
        progress += percent
        print('\rОбработка файлов завершена на %d%%' % progress, end='', flush=True)
        time.sleep(0.01)

m_pbar(1000)