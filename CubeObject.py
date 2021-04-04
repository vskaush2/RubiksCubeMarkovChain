import numpy as np
import copy
from sympy.combinatorics import Permutation


def has_unnecessary_moves(seq):
    for move in ['F','L','U','B','R','D']:
        if 4*move in seq:
            return True
    return False

def delete_redundant_moves(seq):
    while(has_unnecessary_moves(seq)):
        for move in ['F','L','U','B','R','D']:
            if 4*move in seq:
                seq=seq.replace(4*move,'')
    return seq

def get_basic_moves(dim):
    if (dim==2):
        return ['F','L','U','FFF','LLL','UUU']
    else:
        return ['F','L','U','B','R','D']


class CubeObject:
    def __init__(self,cube=None,dim=3):
            #http://iamthecu.be/ labels
            # front=np.array([[1,2,3],[4,5,6],[7,8,9]])
            # left = np.array([[18, 10, 1], [21, 13, 4], [24, 15, 7]])
            # up = np.array([[18, 19, 20], [10, 11, 12], [1, 2, 3]])
            # back=np.array([[20,19,18],[23,22,21],[26,25,24]])
            # right = np.array([[3, 12, 20], [6, 14, 23], [9, 17, 26]])
            # down=np.array([[7,8,9],[15,16,17],[24,25,26]])
        if(cube == None):
            front,left,up,back,right,down=[np.array(np.arange(dim**2*i,dim**2*(i+1))).reshape(dim,dim)
                                           for i in range(6)]
            cube = dict(zip(['Front', 'Left', 'Up', 'Back', 'Right', 'Down'],
                            [front, left, up, back, right, down]))
        self.cube=cube
        self.M=np.eye(dim)[::-1]
        self.dim=dim
        self.permutation=self.get_permutation()
        
    def get_face(self,name):
        return self.cube[name]

    def F(self):
        new_cube = copy.deepcopy(self.cube)
        new_cube['Front']= self.cube['Front'].T@self.M
        new_cube['Left'][:,-1]=self.cube['Down'][0]
        new_cube['Up'][-1] = self.cube['Left'][:,-1]@self.M
        new_cube['Right'][:,0] = self.cube['Up'][-1]
        new_cube['Down'][0]=self.cube['Right'][:,0]@self.M
        return CubeObject(new_cube,self.dim)

    def L(self):
        new_cube = copy.deepcopy(self.cube)
        new_cube['Left']= self.cube['Left'].T@self.M
        new_cube['Back'][:,-1]=self.cube['Down'][:,0]@self.M
        new_cube['Up'][:,0]=self.cube['Back'][:,-1]@self.M
        new_cube['Front'][:,0]=self.cube['Up'][:,0]
        new_cube['Down'][:,0]=self.cube['Front'][:,0]
        return CubeObject(new_cube,self.dim)


    def U(self):
        new_cube = copy.deepcopy(self.cube)
        new_cube['Up']= self.cube['Up'].T@self.M
        new_cube['Front'][0]=self.cube['Right'][0]
        new_cube['Left'][0]=self.cube['Front'][0]
        new_cube['Back'][0]=self.cube['Left'][0]
        new_cube['Right'][0]=self.cube['Back'][0]
        return CubeObject(new_cube,self.dim)

    def B(self):
        new_cube = copy.deepcopy(self.cube)
        new_cube['Back'] = self.cube['Back'].T @ self.M
        new_cube['Right'][:,-1]=self.cube['Down'][-1]@ self.M
        new_cube['Up'][0]=self.cube['Right'][:,-1]
        new_cube['Left'][:,0]=self.cube['Up'][0]@ self.M
        new_cube['Down'][-1]=self.cube['Left'][:,0]
        return CubeObject(new_cube,self.dim)


    def R(self):
        new_cube = copy.deepcopy(self.cube)
        new_cube['Right'] = self.cube['Right'].T @ self.M
        new_cube['Front'][:,-1] =self.cube['Down'][:,-1]
        new_cube['Up'][:,-1] =self.cube['Front'][:,-1]
        new_cube['Back'][:,0] =self.cube['Up'][:,-1] @self.M
        new_cube['Down'][:,-1] =self.cube['Back'][:,0] @self.M
        return CubeObject(new_cube,self.dim)

    def D(self):
        new_cube = copy.deepcopy(self.cube)
        new_cube['Down'] = self.cube['Down'].T @ self.M
        new_cube['Front'][-1]=self.cube['Left'][-1]
        new_cube['Right'][-1]=self.cube['Front'][-1]
        new_cube['Back'][-1]=self.cube['Right'][-1]
        new_cube['Left'][-1]=self.cube['Back'][-1]
        return CubeObject(new_cube,self.dim)



    def rotate(self,seq):
        new_cube=copy.deepcopy(self)
        seq=delete_redundant_moves(seq)
        for move in seq:
            transform_dict={'': new_cube,
                            'F':new_cube.F(),
                            'L':new_cube.L(),
                            'U':new_cube.U(),
                            'B':new_cube.B(),
                            'R':new_cube.R(),
                            'D': new_cube.D()
                            }
            new_cube=transform_dict[move]
        return new_cube

    def get_permutation(self):
        face_matrices=np.array([np.array(value,dtype=int) for value in self.cube.values()])
        sticker_values=face_matrices.reshape(-1).tolist()
        perm=Permutation(sticker_values,size=6*self.dim**2)
        return perm








