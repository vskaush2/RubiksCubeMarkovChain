import numpy as np

face_names=['Front','Left','Up','Back','Right','Down']
basic_moves=['F','L','U','B','R','D']
move_dict=dict(zip(basic_moves, face_names))

# iamthecube_configuration={'Front': np.array([1,2,3,4,5,6,7,8,9]).reshape(3,3),
#                           'Left': np.array([18,10,1,21,13,4,24,15,7]).reshape(3,3),
#                           'Up': np.array([18,19,20,10,11,12,1,2,3]).reshape(3,3),
#                           'Back': np.array([20,19,18,23,22,21,26,25,24]).reshape(3,3),
#                           'Right': np.array([3,12,20,6,14,23,9,17,26]).reshape(3,3),
#                           'Down': np.array([7,8,9,15,16,17,24,25,26]).reshape(3,3)}
# iamthecube_configuration # https://iamthecu.be/.com

def delete_unnecessary_moves(move_seq,n):
    if n==2:
        move_seq= move_seq.replace("B",'FFF').replace("R",'LLL').replace("D",'UUU') # Special Move Replacements for dimension 2
    while True:
        try:
            unnecessary_move=next(basic_move for basic_move in basic_moves if 4*basic_move in move_seq) # Removing any 4 consecutive face rotations of the same type
            move_seq = move_seq.replace(4*unnecessary_move,'')
        except:
            return move_seq

def configurations_are_equal(configuration1_dict,configuration2_dict):
    for key in configuration1_dict.keys():
        if list(configuration1_dict[key].reshape(-1)) != list(configuration2_dict[key].reshape(-1)):
            return False
    return True


def plot_configuration(configuration_dict,
                       title='',
                       colors_dict=None,
                       linewidth=4.0,
                       edgecolor='black',
                       alpha=1,
                       show_front_faces=True,
                       show_left_faces=True,
                       show_up_faces=True,
                       show_back_faces=True,
                       show_right_faces=True,
                       show_down_faces=True,
                       show_front_labels=False,
                       show_left_labels=False,
                       show_up_labels=False,
                       show_back_labels=False,
                       show_right_labels=False,
                       show_down_labels=False):
    fig = plt.figure(figsize=(5, 5))
    ax = plt.axes(projection='3d')
    n = len(configuration_dict['Front'])

    if colors_dict == None:
        colors = n ** 2 * ['white'] + n ** 2 * ['blue'] + n ** 2 * ['red'] + n ** 2 * ['green'] + n ** 2 * [
            'orange'] + n ** 2 * ['yellow']
        colors_dict = dict(zip(range(6 * n ** 2), colors))

    front_squares = [np.array([[i, 0, n - j], [i + 1, 0, n - j], [i + 1, 0, n - j - 1], [i, 0, n - j - 1]]) for j in
                     range(n) for i in range(n)]
    if show_front_faces:
        for i in range(len(front_squares)):
            square = front_squares[i]
            label = configuration_dict['Front'].flatten()[i]
            color = colors_dict[label]
            center = np.mean(square, axis=0)  # Center of Square
            ax.add_collection3d(Poly3DCollection([square],
                                                 facecolor=color,
                                                 linewidths=linewidth,
                                                 edgecolors=edgecolor,
                                                 alpha=alpha))
            if show_front_labels:
                ax.text3D(center[0], center[1], center[2], label, zdir='x')

    back_squares = [
        np.array([[n - i, n, n - j], [n - (i + 1), n, n - j], [n - (i + 1), n, n - j - 1], [n - i, n, n - j - 1]]) for j
        in range(n) for i in range(n)]
    if show_back_faces:
        for i in range(len(back_squares)):
            square = back_squares[i]
            label = configuration_dict['Back'].flatten()[i]
            color = colors_dict[label]
            center = np.mean(square, axis=0)  # Center of Square
            ax.add_collection3d(Poly3DCollection([square],
                                                 facecolor=color,
                                                 linewidths=linewidth,
                                                 edgecolors=edgecolor,
                                                 alpha=alpha))
            if show_back_labels:
                ax.text3D(center[0], center[1], center[2], label, zdir='x')

    left_squares = [
        np.array([[0, n - i - 1, n - j], [0, n - i, n - j], [0, n - i, n - j - 1], [0, n - (i + 1), n - j - 1]]) for j
        in range(n) for i in range(n)]
    if show_left_faces:
        for i in range(len(left_squares)):
            square = left_squares[i]
            label = configuration_dict['Left'].flatten()[i]
            color = colors_dict[label]
            center = np.mean(square, axis=0)  # Center of Square
            ax.add_collection3d(Poly3DCollection([square],
                                                 facecolor=color,
                                                 linewidths=linewidth,
                                                 edgecolors=edgecolor,
                                                 alpha=alpha))
            if show_left_labels:
                ax.text3D(center[0], center[1], center[2], label, zdir='y')

    right_squares = [np.array([[n, i, n - j], [n, i + 1, n - j], [n, i + 1, n - j - 1], [n, i, n - j - 1]]) for j in
                     range(n) for i in range(n)]
    if show_right_faces:
        for i in range(len(right_squares)):
            square = right_squares[i]
            label = configuration_dict['Right'].flatten()[i]
            color = colors_dict[label]
            center = np.mean(square, axis=0)  # Center of Square
            ax.add_collection3d(Poly3DCollection([square],
                                                 facecolor=color,
                                                 linewidths=linewidth,
                                                 edgecolors=edgecolor,
                                                 alpha=alpha))
            if show_right_labels:
                ax.text3D(center[0], center[1], center[2], label, zdir='y')

    down_squares = [np.array([[i, j, 0], [i + 1, j, 0], [i + 1, j + 1, 0], [i, j + 1, 0]]) for j in range(n) for i in
                    range(n)]
    if show_down_faces:
        for i in range(len(down_squares)):
            square = down_squares[i]
            label = configuration_dict['Down'].flatten()[i]
            color = colors_dict[label]
            center = np.mean(square, axis=0)  # Center of Square
            ax.add_collection3d(Poly3DCollection([square],
                                                 facecolor=color,
                                                 linewidths=linewidth,
                                                 edgecolors=edgecolor,
                                                 alpha=alpha))
            if show_down_labels:
                ax.text3D(center[0], center[1], center[2], label, zdir='x')

    up_squares = [np.array([[i, n - j, n], [i + 1, n - j, n], [i + 1, n - (j + 1), n], [i, n - (j + 1), n]]) for j in
                  range(n) for i in range(n)]
    if show_up_faces:
        for i in range(len(up_squares)):
            square = up_squares[i]
            label = configuration_dict['Up'].flatten()[i]
            color = colors_dict[label]
            center = np.mean(square, axis=0)  # Center of Square
            ax.add_collection3d(Poly3DCollection([square],
                                                 facecolor=color,
                                                 linewidths=linewidth,
                                                 edgecolors=edgecolor,
                                                 alpha=alpha))
            if show_up_labels:
                ax.text3D(center[0], center[1], center[2], label, zdir='x')

    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_zlim(0, n)
    ax.axis('off')
    ax.set_title(title)
    plt.close()
    return fig


class CubeConfiguration:

    def __init__(self, n, configuration_dict=None):
        self.n=n
        if configuration_dict == None:
            configuration_dict=self.get_solved_cube_configuration_dict()

        self.configuration_dict=configuration_dict

    def get_solved_cube_configuration_dict(self):
        face_matrices = [np.arange(j * self.n ** 2, (j + 1) * self.n ** 2).reshape(self.n, self.n) for j in range(6)]
        solved_cube_configuration_dict = dict(zip(face_names, face_matrices))
        return solved_cube_configuration_dict

    def rotate_face(self, face_name):
        old_front, old_left, old_up, old_back, old_right, old_down = [face_matrix.copy() for face_matrix in
                                                                      self.configuration_dict.values()]
        new_front, new_left, new_up, new_back, new_right, new_down = [face_matrix.copy() for face_matrix in
                                                                      self.configuration_dict.values()]

        if face_name == 'Front':
            new_front = old_front[::-1].T
            new_up[-1] = old_left[:, -1][::-1]
            new_right[:, 0] = old_up[-1]
            new_down[0] = old_right[:, 0][::-1]
            new_left[:, -1] = old_down[0]

        if face_name == 'Left':
            new_left = old_left[::-1].T
            new_up[:, 0] = old_back[:, -1][::-1]
            new_front[:, 0] = old_up[:, 0]
            new_down[:, 0] = old_front[:, 0]
            new_back[:, -1] = old_down[:, 0][::-1]

        if face_name == 'Up':
            new_up = old_up[::-1].T
            new_back[0] = old_left[0]
            new_right[0] = old_back[0]
            new_front[0] = old_right[0]
            new_left[0] = old_front[0]

        if face_name == 'Back':
            new_back = old_back[::-1].T
            new_up[0] = old_right[:, -1]
            new_left[:, 0] = old_up[0][::-1]
            new_down[-1] = old_left[:, 0]
            new_right[:, -1] = old_down[-1][::-1]

        if face_name == 'Right':
            new_right = new_right[::-1].T
            new_up[:, -1] = old_front[:, -1]
            new_back[:, 0] = old_up[:, -1][::-1]
            new_down[:, -1] = old_back[:, 0][::-1]
            new_front[:, -1] = old_down[:, -1]

        if face_name == 'Down':
            new_down = new_down[::-1].T
            new_front[-1] = old_left[-1]
            new_right[-1] = old_front[-1]
            new_back[-1] = old_right[-1]
            new_left[-1] = old_back[-1]

        new_configuration_dict = dict(zip(face_names, [new_front, new_left, new_up, new_back, new_right, new_down]))
        return new_configuration_dict

    def move(self, move_seq):
        move_seq = delete_unnecessary_moves(move_seq, self.n)
        new_configuration_dict = self.configuration_dict
        if move_seq != '':
            for move in move_seq:
                new_configuration_dict = CubeConfiguration(self.n,new_configuration_dict).rotate_face(move_dict[move])
        return new_configuration_dict








