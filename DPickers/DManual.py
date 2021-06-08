# -------------------------------------------------------------------
# Manual picker.
#
# Author: Liang Ding
# Email: myliang.ding@mail.utoronto.ca
# -------------------------------------------------------------------


from DPickers import DL_NO_VALUE
import numpy as np
import matplotlib.pyplot as plt


def normalize(data_array):
    '''Normalize the data in group.'''

    num_tr = data_array.__len__()
    for tr in range(num_tr):
        if data_array[tr].__len__() == 0:
            # get ride of empty trace.
            continue
        if np.max(np.fabs(data_array[tr])) <1e-6:
            continue
        data_array[tr] = 0.5 * data_array[tr] / np.max(np.fabs(data_array[tr]))
    return data_array


class DMPicker(object):
    '''First break picking manually.'''
    def __init__(self, ax, data_array, t0, dt, save_path=None):
        self.ax = ax
        self.lx = ax.axhline(color='C0')  # the horiz line
        self.ly = ax.axvline(color='C0')  # the vert line
        self.ntraces, self.npts = data_array.shape

        if self.ntraces < 1:
            raise IndexError("NO TRACE.")
        if self.npts < 1:
            raise IndexError("NO DATA.")

        self.dt = dt
        self.x = np.linspace(0, self.dt * self.npts, self.npts)
        self.data_array = data_array
        # self.lw = np.max(self.data_array[0]) / 2
        self.lw = 0.5  # label width.

        # containers
        self.trcs_picks = []
        self.trcs_lines = []
        for _ in range(self.ntraces):
            self.trcs_picks.append([])
            self.trcs_lines.append([])
        # text location in axes coords
        self.txt = ax.text(0.7, 0.95, '', transform=ax.transAxes)
        self.t0 = t0
        self.ERROR = dt /10
        self.NEAR_WINDOW = 20
        # file operation
        self.save_path = save_path



    def mouse_move(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        idx_tr = min(int(y), self.ntraces)       # get trace number
        if idx_tr <= 0:
            idx_tr = 1
        idx_x = min(np.searchsorted(self.x, [x])[0], len(self.x) - 1)
        x = self.x[idx_x]
        y = self.data_array[idx_tr-1][idx_x] + idx_tr
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)
        self.txt.set_text('sensor=%d, time=%1.2f' % (idx_tr, x))
        plt.draw()


    def _check_in(self, x, data):
        '''Checking whether the x is in the pikings.'''

        for idx, each in enumerate(data):
            if np.fabs(x-each) < self.ERROR:
                return True, idx

        return False, None


    def _check_near(self, x, data):
        '''Checking whether the x is near a picking.'''
        for idx, each in enumerate(data):
            if np.fabs(x - each) < self.NEAR_WINDOW * self.dt:
                return True, idx, each

        return False, None, None


    def _click_left_button(self, event):
        '''Interactive of left button clicking event.'''
        x, y = event.xdata, event.ydata

        idx_tr = min(int(y), self.ntraces)  # get trace number
        if idx_tr <= 0:
            idx_tr = 1

        idx_x = min(np.searchsorted(self.x, [x])[0], len(self.x) - 1)
        x = self.x[idx_x]
        y = self.data_array[idx_tr - 1][idx_x] + idx_tr
        b_check, i = self._check_in(x, self.trcs_picks[idx_tr - 1])
        if b_check:
            line_obj = self.trcs_lines[idx_tr - 1][i]
            self.trcs_lines[idx_tr - 1].remove(line_obj)  # remove the line object from the line_list.
            line_obj.remove()  # remove the line from the figure.
            self.trcs_picks[idx_tr - 1].remove(x)  # remove the picking time.

        else:
            b_near, j, near_x = self._check_near(x, self.trcs_picks[idx_tr - 1])
            if b_near:
                line_obj = self.trcs_lines[idx_tr - 1][j]
                self.trcs_lines[idx_tr - 1].remove(line_obj)
                line_obj.remove()
                self.trcs_picks[idx_tr - 1].remove(near_x)

            self.trcs_picks[idx_tr - 1].append(x)
            line_obj = plt.plot([x, x], [y - self.lw, y + self.lw], 'r--')
            self.trcs_lines[idx_tr - 1].append(line_obj[0])

        plt.draw()



    def mouse_click(self, event):
        '''Interactive for mouse (button) clicking event.'''
        if not event.inaxes:
            return

        if 1 == event.button:
            self._click_left_button(event)


    def _press_w(self, event):
        '''Press 'w' to save the picking results. '''

        if self.save_path is None:
            # TODO: code for making dir and create file.
            return

        # Allow writing one event.
        # TODO: write more events.
        picking_time = []

        for idx_tr in range(self.ntraces):
            if self.trcs_picks[idx_tr].__len__() == 0:
                picking_time.append(DL_NO_VALUE)
                continue

            else:
                t_str = self.trcs_picks[idx_tr][0]
                picking_time.append(t_str)
        with open(self.save_path, 'a') as fw:
            fw.write(str(self.t0))
            fw.write(", ")
            for pk in picking_time:
                fw.write(str(np.round(pk, 7))+str(', '))
            fw.write('\n')

        # show information.
        self.ax.set_title("Saved!", color='r')
        plt.draw()


    def _press_ctrl_alt_d(self, event):
        '''Delete all pickings.'''
        for idx_tr in range(self.ntraces):
            for line_obj in self.trcs_lines[idx_tr]:
                line_obj.remove()
            self.trcs_lines[idx_tr].clear()
            self.trcs_picks[idx_tr].clear()
        self.ax.set_title('')
        plt.draw()


    def key_press(self, event):
        '''Interactive for key pressing event.'''
        if not event.inaxes:
            return

        # press 'w' (lower case) to save the picking.
        if 'w' == event.key:
            self._press_w(event)

        if 'ctrl+alt+d' == event.key:
            self._press_ctrl_alt_d(event)


class DMPickerWnd():
    '''The window instance of Manual Picker.'''

    def __init__(self, data_array, t0, dt, save_path,
                 wave_color='C7', amp_scale=1.0,
                 b_fill=False, wiggle_color='C7',
                 fig=None, ax=None):

        if fig is None or ax is None:
            self.fig, self.ax = plt.subplots()
        else:
            self.ax = ax
            self.fig = fig

        self.ntraces, self.npts = data_array.shape
        if self.ntraces < 1:
            raise IndexError("NO TRACE.")
        if self.npts < 1:
            raise IndexError("NO DATA.")

        self.dt = dt
        self.t = np.linspace(0, self.dt * self.npts, self.npts)

        self.wave_color = wave_color
        self.amp_scale = amp_scale
        self.b_fill = b_fill
        self.wiggle_color = wiggle_color

        self.cursor = DMPicker(self.ax, data_array, t0, dt, save_path)

        # fig.canvas.mpl_connect('button_press_event', mouse_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.cursor.mouse_move)
        self.fig.canvas.mpl_connect('button_press_event', self.cursor.mouse_click)
        self.fig.canvas.mpl_connect('key_press_event', self.cursor.key_press)

        # initialize the window and pick.
        self.set_Wnd(data_array)


    def set_Wnd(self, data_array):
        '''Initialize the window for picking. '''

        data = normalize(data_array)

        amp = 1.  # normalization factor
        gmin = 0.  # global minimum
        toffset = 0.  # offset in time to make 0 centered

        self.ax.set_xlim(0, max(self.t))
        self.ax.set_xlabel("Time")
        y0 = 1
        y1 = self.ntraces + 1
        dy = 1

        self.ax.set_ylim(y1, y0 - 1)
        self.ax.set_ylabel("Trace Number")
        for i, trace in enumerate(data):
            tr = (((trace - gmin) / amp) - toffset) * self.amp_scale * dy
            y = y0 + i * dy  # x positon for this trace
            self.ax.plot(self.t, y + tr, color=self.wave_color)
            if self.b_fill:
                self.ax.fill_between(self.t, y, y + tr, tr > 0, color=self.wiggle_color)

        plt.tight_layout()
        plt.show()










