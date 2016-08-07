import functools


def memoize_args(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        if args not in cache:
            try:
                ret = obj(*args, **kwargs)
            except Exception as e:
                ret = e
            finally:
                cache[args] = ret
        ret = cache[args]
        if isinstance(ret, Exception):
            raise ret
        return ret
    return memoizer