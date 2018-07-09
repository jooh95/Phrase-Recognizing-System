import java.awt.List;
import java.awt.Robot;
import java.util.ArrayList;

import com.sun.jna.Native;
import com.sun.jna.Pointer;
import com.sun.jna.platform.win32.*;
import com.sun.jna.platform.win32.Netapi32Util.User;
import com.sun.jna.platform.win32.WinDef.HDC;
import com.sun.jna.platform.win32.WinDef.HWND;
import com.sun.jna.platform.win32.WinDef.RECT;
import com.sun.jna.platform.win32.WinUser.WNDENUMPROC;

public class GetHandler {

 public static void main(String[] args) {
  
  try{
   
   User32.INSTANCE.EnumWindows(new WNDENUMPROC() {
             int count = 0;
             public boolean callback(HWND hWnd, Pointer arg1) {
                 char[] windowText = new char[512];
                 User32.INSTANCE.GetWindowText(hWnd, windowText, 512);
                 String wText = Native.toString(windowText);
                 RECT rectangle = new RECT();
                 User32.INSTANCE.GetWindowRect(hWnd, rectangle);
                 // get rid of this if block if you want all windows regardless
                 // of whether
                 // or not they have text
                 // second condition is for visible and non minimised windows
                 if (wText.isEmpty() || !(User32.INSTANCE.IsWindowVisible(hWnd)
                         && rectangle.left > -32000)) {
                     return true;
                 }

                 char[] c=new char[512];
                 User32.INSTANCE.GetClassName(hWnd, c, 512);
                 String clsName=String.valueOf(c).trim();

                 System.out.println(
                   //"hwnd:"+hWnd+","+
                         "Number:" + (++count) + ",Text:" + wText+","+
                         "Position:("+rectangle.left+","+rectangle.top+")~("+rectangle.right+","+rectangle.bottom+"),"+
                         "Class Name:"+clsName);
                 
                 return true;
             }
         }, null);
   
  }catch(Exception ex){System.out.println(ex.getMessage());}
 }

}
