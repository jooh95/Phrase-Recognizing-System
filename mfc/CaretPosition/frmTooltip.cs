
//////////////////////////////////////////////////////////////////////////
//                                                                      //
//  Anybody can Use, Modify, Redistribute this code freely. If this     // 
//  module has been helpful to you then just leave a comment on Website //
//                                                                      //
//////////////////////////////////////////////////////////////////////////


using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Runtime.InteropServices;
using System.Threading;
using System.Diagnostics;
using System.Windows.Forms;

namespace CaretPosition
{
    public partial class frmTooltip : Form
    {

       public frmTooltip()
       {
           InitializeComponent();
           timer1.Start();  // Processing events from Hooks involves message queue complexities.
       }                    // Timer has been used just to avoid that Mouse and Keyboard hooking                           
                            // and to keep things simple. 

       # region Data Members & Structures 
               
            
           
            [StructLayout(LayoutKind.Sequential)]    // Required by user32.dll
            public struct RECT
            {
                public uint Left;
                public uint Top;
                public uint Right;
                public uint Bottom;
            };

            [StructLayout(LayoutKind.Sequential)]    // Required by user32.dll
            public struct GUITHREADINFO
            {
                public uint cbSize;
                public uint flags;
                public IntPtr hwndActive;
                public IntPtr hwndFocus;
                public IntPtr hwndCapture;
                public IntPtr hwndMenuOwner;
                public IntPtr hwndMoveSize;
                public IntPtr hwndCaret;
                public RECT rcCaret;
            };                  

            Point startPosition = new Point();       // Point required for ToolTip movement by Mouse
            GUITHREADINFO guiInfo;                     // To store GUI Thread Information
            Point caretPosition;                     // To store Caret Position  
        

        # endregion

       # region DllImports 
        

           /*- Retrieves Title Information of the specified window -*/
           [DllImport("user32.dll")]
           static extern int GetWindowText(int hWnd, StringBuilder text, int count);

           /*- Retrieves Id of the thread that created the specified window -*/
           [DllImport("user32.dll", SetLastError = true)]
           static extern uint GetWindowThreadProcessId(int hWnd, out uint lpdwProcessId);

           /*- Retrieves information about active window or any specific GUI thread -*/
           [DllImport("user32.dll", EntryPoint = "GetGUIThreadInfo")]     
           public static extern bool GetGUIThreadInfo(uint tId, out GUITHREADINFO threadInfo);

           /*- Retrieves Handle to the ForeGroundWindow -*/
           [DllImport("user32.dll")]         
           public static extern IntPtr GetForegroundWindow();

           /*- Converts window specific point to screen specific -*/
           [DllImport("user32.dll")]       
           public static extern bool ClientToScreen(IntPtr hWnd, out Point position);
        [System.Runtime.InteropServices.DllImport("user32.dll", SetLastError = true, CharSet = System.Runtime.InteropServices.CharSet.Auto)]
        public static extern int RegisterWindowMessage(string lpString);

        [System.Runtime.InteropServices.DllImport("user32.dll", EntryPoint = "SendMessage", CharSet = System.Runtime.InteropServices.CharSet.Auto)] //
        public static extern bool SendMessage(IntPtr hWnd, uint Msg, int wParam, StringBuilder lParam);
        [System.Runtime.InteropServices.DllImport("user32.dll", SetLastError = true)]
        public static extern IntPtr SendMessage(int hWnd, int Msg, int wparam,
      int lparam);
        [DllImport("user32.dll", EntryPoint = "GetWindowText",
  CharSet = CharSet.Auto)]
        static extern IntPtr GetWindowCaption(IntPtr hwnd,
  StringBuilder lpString, int maxCount);
        [DllImport("user32.dll", EntryPoint = "SendMessage",
  CharSet = CharSet.Auto)]
        static extern int SendMessage3(IntPtr hwndControl, uint Msg,
  int wParam, StringBuilder strBuffer); // get text

        [DllImport("user32.dll", EntryPoint = "SendMessage",
          CharSet = CharSet.Auto)]
        static extern int SendMessage4(IntPtr hwndControl, uint Msg,
          int wParam, int lParam);  // text length


        private const int WM_GETTEXT = 0x000D;
        private const int WM_SETTEXT = 0x000C;
        private const int WM_GETTEXTLENGTH = 0x000E;
      





        //static string GetWindowCaption(IntPtr hwnd)
        //{
        //    StringBuilder sb = new StringBuilder(256);
        //    GetWindowCaption(hwnd, sb, 256);
        //    return sb.ToString();
        //}

        //const int WM_GETTEXT = 0x000D;
        //const int WM_GETTEXTLENGTH = 0x000E;

        //#endregion

        //#region Event Handlers 

        //public void RegisterControlforMessages()
        //{
        //    RegisterWindowMessage("WM_GETTEXT");
        //}
        //public string GetControlText(IntPtr hWnd)
        //{

        //    StringBuilder title = new StringBuilder();

        //    // Get the size of the string required to hold the window title. 
        //    Int32 size = SendMessage((int)hWnd, WM_GETTEXTLENGTH, 0, 0).ToInt32();

        //    // If the return is 0, there is no title. 
        //    if (size > 0)
        //    {
        //        title = new StringBuilder(size + 1);

        //        SendMessage(hWnd, (int)WM_GETTEXT, title.Capacity, title);


        //    }
        //    return title.ToString();
        //}


        static int GetTextBoxTextLength(IntPtr hTextBox)
        {
            // helper for GetTextBoxText
            uint WM_GETTEXTLENGTH = 0x000E;
            int result = SendMessage4(hTextBox, WM_GETTEXTLENGTH,
              0, 0);
            return result;
        }

        static string GetTextBoxText(IntPtr hTextBox)
        {
            uint WM_GETTEXT = 0x000D;
            int len = GetTextBoxTextLength(hTextBox);
            if (len <= 0) return null;  // no text
            StringBuilder sb = new StringBuilder(len + 1);
            SendMessage3(hTextBox, WM_GETTEXT, len + 1, sb);
            return sb.ToString();
        }


        private void timer1_Tick(object sender, EventArgs e)
           {

            // If Tooltip window is active window (Suppose user clicks on the Tooltip Window)
            if (GetForegroundWindow() == this.Handle)
               {
                   // then do no processing
                   return;
               }

               // Get Current active Process
               string activeProcess = GetActiveProcess();

               // If window explorer is active window (eg. user has opened any drive)
               // Or for any failure when activeProcess is nothing               
               if ((activeProcess.ToLower().Contains("explorer") | (activeProcess == string.Empty)))
               {
                   // Dissappear Tooltip
                   this.Visible = false;
               }
               else
               {
                   // Otherwise Calculate Caret position
                   EvaluateCaretPosition();

                   // Adjust ToolTip according to the Caret
                   AdjustUI();

                // Display current active Process on Tooltip
                //string ho = GetControlText(GetForegroundWindow());

                //// needs to be big enough for the whole text
                string caption = GetTextBoxText(GetForegroundWindow());
                lblCurrentApp.Text = " You are Currently inside : " + caption  + " : "+ activeProcess;
                   this.Visible = true;
               }               
           }

           private void panel1_MouseEnter(object sender, EventArgs e)
           {
               // Set the Mouse Cursor
               this.Cursor = Cursors.SizeAll;
           }

           private void panel1_MouseMove(object sender, MouseEventArgs e)
           {
               // If Left Button was pressed
               if (e.Button == MouseButtons.Left)
               {
                   // then move the Tooltip
                   this.Left += e.Location.X - startPosition.X;
                   this.Top += e.Location.Y - startPosition.Y;
               }
           }

           private void panel1_MouseDown(object sender, MouseEventArgs e)
           {
               // Store start position of mouse when clicked down.
               // It will be used to calculate offset during movement.
               startPosition = e.Location;
           }


       #endregion

       #region Methods 
        

        
           /// <summary>
           /// This function will adjust Tooltip position and
           /// will keep it always inside the screen area.
           /// </summary>
           private void AdjustUI()
           {
               // Get Current Screen Resolution
               Rectangle workingArea = SystemInformation.WorkingArea;

               // If current caret position throws Tooltip outside of screen area
               // then do some UI adjustment.
               if (caretPosition.X + this.Width > workingArea.Width)
               {
                   caretPosition.X = caretPosition.X - this.Width - 50;
               }

               if (caretPosition.Y + this.Height > workingArea.Height)
               {
                   caretPosition.Y = caretPosition.Y - this.Height - 50;
               }

               this.Left = caretPosition.X;
               this.Top = caretPosition.Y;
           }

           /// <summary>
           /// Evaluates Cursor Position with respect to client screen.
           /// </summary>
           private void EvaluateCaretPosition()
           {
               caretPosition = new Point();                 

               // Fetch GUITHREADINFO
               GetCaretPosition();

               caretPosition.X = (int)guiInfo.rcCaret.Left + 25;
               caretPosition.Y = (int)guiInfo.rcCaret.Bottom + 25;

               ClientToScreen(guiInfo.hwndCaret, out caretPosition);

               txtCaretX.Text = (caretPosition.X).ToString();
               txtCaretY.Text = caretPosition.Y.ToString();

           }

           /// <summary>
           /// Get the caret position
           /// </summary>
           public void GetCaretPosition()
           {
               guiInfo = new GUITHREADINFO();
               guiInfo.cbSize = (uint)Marshal.SizeOf(guiInfo);

               // Get GuiThreadInfo into guiInfo
               GetGUIThreadInfo(0, out guiInfo);
           }              
     
           /// <summary>
           /// Retrieves name of active Process.
           /// </summary>
           /// <returns>Active Process Name</returns>
           private string GetActiveProcess()
           {
               const int nChars = 256;
               int handle = 0;
               StringBuilder Buff = new StringBuilder(nChars);
               handle = (int)GetForegroundWindow();

               // If Active window has some title info
               if (GetWindowText(handle, Buff, nChars) > 0)
               {
                   uint lpdwProcessId;
                   uint dwCaretID = GetWindowThreadProcessId(handle, out lpdwProcessId);
                   uint dwCurrentID = (uint)Thread.CurrentThread.ManagedThreadId;
                   return Process.GetProcessById((int)lpdwProcessId).ProcessName;
               }
               // Otherwise either error or non client region
               return String.Empty;
           }




        #endregion

        private void panel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private void txtCaretX_TextChanged(object sender, EventArgs e)
        {

        }
    }
}
