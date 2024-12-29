from concurrent.futures import ThreadPoolExecutor


class Pool(object):       # 数据库连接池
    __pool = None     # 记录第一个被创建的对象引用
    def __new__(cls, *args, **kwargs):
        """创建连接池对象  单例设计模式(每个线程中只创建一个连接池对象)  PersistentDB为每个线程提供专用的连接池"""
        if cls.__pool is None:    # 如果__pool为空，说明创建的是第一个连接池对象
            cls.__pool = ThreadPoolExecutor(max_workers=100)
        return cls.__pool