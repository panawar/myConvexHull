"""
# implementasi convex hull dengan algoritma devide and conquer
# @author Panawar Hasibuan
# @email 13517129@std.stei.itb.ac.id
"""
import numpy as np

class MyConvexHull:
    """
    data: numpy.array(N,2)
    """
    def __init__(self, bucket):
        self.bucket = np.copy(bucket)
        x = np.copy(self.bucket)
        x = x[x[:,1].argsort()]
        self.sorted = x[x[:,0].argsort(kind='mergesort')]
        self.simplices =self.hull(self.setIdx(self.sorted))
    
    """
    Algoritma Devide and Conquer
    prekondisi, data terurut
    return, set index penyusun convex hull
    """
    def DnC(self,data,state):
        hull = np.unique([-99])
        if len(data) > 3:
            #rekurens
            #simpan pembentuk convexhull
            q = np.copy(data[0])
            r = np.copy(data[-1])
            hull = np.union1d(self.getIdx(q),self.getIdx(r))
            #Karna state awal True, dan data terurut terhadap x
            #urutkan data
            if not state: 
                #terurut terhadap x
                data = data[data[:,1].argsort()]
                data = data[data[:,0].argsort(kind='mergesort')]
            else:
                #terurut terhadap y
                data = data[data[:,0].argsort()]
                data = data[data[:,1].argsort(kind='mergesort')]

            if (r[0]==data[0,0] and r[1]==data[0,1]) or (q[0]==data[0,0] and q[1]==data[0,1]): #r==data[0] or q==data[0]
                p = np.copy(data[-1])
            else:
                p = np.copy(data[0])
            first = np.array((p,q),dtype=int) #menampung titik kelompok 1
            second = np.array((p,r),dtype=int) #menampung titik kelompok 2
            for i in range(1,len(data)-1):
                if self.isBesideQ(data[i],p,q,r):
                    first = np.vstack((first,np.copy(data[i])))
                elif self.isBesideR(data[i],p,q,r):
                    second = np.vstack((second,np.copy(data[i])))
            hull = np.union1d(hull,self.DnC(first,not state))
            hull = np.union1d(hull,self.DnC(second,not state))
        else:
            #kondisi stop
            for e in data:
                hull = np.union1d(hull,self.getIdx(e))
        return hull

    

    """
    cek apakah  titik point terletak berlawanan dengan r terhadap garis yang menghubungkan p dan q
    proses mendapat perhitungan di algoritma ini ada di laporan
    """
    def isBesideR(self,point,p,q,r):
        x1,y1 = p[0],p[1]
        x2,y2 = r[0],r[1]
        if x1 == x2: #garis lurus horizontal
            return (point[0]-x1)*(q[0]-x1) < 0
        elif y1 == y2: #garis lurus vertikal
            return (point[1]-y1)*(q[1]-y1) < 0
        else:                
            fpoint=point[1]*(x2-x1)
            xpoint=point[0]*(y2-y1)+y1*(x2-x1)-x1*(y2-y1)
            fq=q[1]*(x2-x1)
            xq=q[0]*(y2-y1)+y1*(x2-x1)-x1*(y2-y1)
            return (fpoint-xpoint)*(fq-xq)<0

    """
    cek apakah  titik point terletak berlawanan dengan r terhadap garis yang menghubungkan p dan q
    proses mendapat perhitungan di algoritma ini ada di laporan
    """
    def isBesideQ(self,point,p,q,r):    
        x1,y1 = p[0],p[1]
        x2,y2 = q[0],q[1]
        if x1 == x2: #garis lurus horizontal
            return (point[0]-x1)*(r[0]-x1) < 0
        elif y1 == y2: #garis lurus vertikal
            return (point[1]-y1)*(r[1]-y1) < 0
        else:
            fpoint=point[1]*(x2-x1)
            xpoint=point[0]*(y2-y1)+y1*(x2-x1)-x1*(y2-y1)
            fr=r[1]*(x2-x1)
            xr=r[0]*(y2-y1)+y1*(x2-x1)-x1*(y2-y1)
            return (fpoint-xpoint)*(fr-xr)<0

    """
    Mengembalikan index dari data di self.bucket
    mengembalikan -1 jika data tidak ada di self.bcuket
    """
    def getIdx(self,data):
        for i in range(len(self.bucket)):
            if self.bucket[i][0]== data[0] and self.bucket[i][1]==data[1]:
                return i
                break
            elif i == len(self.bucket)-1:
                return -1

    """
    prekondisi: data terurut
    membagi data menjadi dua, up dan down, dipisahkan oleh data[0] dan data[-1]
    """
    def devide(self,data,up,down):
        x1,y1 = data[0,0],data[0,1]
        x2,y2 = data[-1,0],data[-1,1]
        i = 1
        while i < len(data)-1:
            p = data[i]
            if x1 == x2: #garis lurus horizontal
                if (p[0]-x1) < 0:
                    #up
                    up = np.vstack((up,p))
                else:
                    #down
                    down = np.vstack((down,p))
            elif y1 == y2: #garis lurus vertikal
                if (p[1]-y1) < 0:
                    #up
                    up = np.vstack((up,p))
                else:
                    #down
                    down = np.vstack((down,p))
            else:                
                fp=p[1]*(x2-x1)
                xp=p[0]*(y2-y1)+y1*(x2-x1)-x1*(y2-y1)
                if (fp-xp)<0:
                    #up
                    up = np.vstack((up,p))
                else:
                    #down
                    down = np.vstack((down,p))
            i = i+1
        up = np.vstack((up,data[-1]))
        down = np.vstack((down,data[-1]))

    """
    Mengembalikan himpunan index dari pembangun vertex hull
    """
    def setIdx(self,sort):
        up = np.array(sort[0])
        down = np.array(sort[0])
        self.devide(sort,up,down)
        return np.union1d(self.DnC(up,True),self.DnC(down,True))

    """
    Mengembalikan ndarray index pembangun vertex hull, berbentuk simplices
    """
    def hull(self,set):
        return set
