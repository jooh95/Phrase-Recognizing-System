namespace CaretPosition
{
    partial class frmTooltip
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.timer1 = new System.Windows.Forms.Timer(this.components);
            this.lblCaretX = new System.Windows.Forms.Label();
            this.lblCaretY = new System.Windows.Forms.Label();
            this.panel1 = new System.Windows.Forms.Panel();
            this.lblCurrentApp = new System.Windows.Forms.Label();
            this.txtCaretX = new System.Windows.Forms.TextBox();
            this.txtCaretY = new System.Windows.Forms.TextBox();
            this.SuspendLayout();
            // 
            // timer1
            // 
            this.timer1.Enabled = true;
            this.timer1.Interval = 200;
            this.timer1.Tick += new System.EventHandler(this.timer1_Tick);
            // 
            // lblCaretX
            // 
            this.lblCaretX.AutoSize = true;
            this.lblCaretX.BackColor = System.Drawing.Color.Transparent;
            this.lblCaretX.Enabled = false;
            this.lblCaretX.Location = new System.Drawing.Point(30, 14);
            this.lblCaretX.Name = "lblCaretX";
            this.lblCaretX.Size = new System.Drawing.Size(55, 12);
            this.lblCaretX.TabIndex = 3;
            this.lblCaretX.Text = "Caret X :";
            // 
            // lblCaretY
            // 
            this.lblCaretY.AutoSize = true;
            this.lblCaretY.BackColor = System.Drawing.Color.Transparent;
            this.lblCaretY.Enabled = false;
            this.lblCaretY.Location = new System.Drawing.Point(30, 46);
            this.lblCaretY.Name = "lblCaretY";
            this.lblCaretY.Size = new System.Drawing.Size(55, 12);
            this.lblCaretY.TabIndex = 4;
            this.lblCaretY.Text = "Caret Y :";
            // 
            // panel1
            // 
            this.panel1.BackColor = System.Drawing.Color.Transparent;
            this.panel1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.panel1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panel1.Location = new System.Drawing.Point(0, 0);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(328, 93);
            this.panel1.TabIndex = 6;
            this.panel1.Paint += new System.Windows.Forms.PaintEventHandler(this.panel1_Paint);
            this.panel1.MouseDown += new System.Windows.Forms.MouseEventHandler(this.panel1_MouseDown);
            this.panel1.MouseEnter += new System.EventHandler(this.panel1_MouseEnter);
            this.panel1.MouseMove += new System.Windows.Forms.MouseEventHandler(this.panel1_MouseMove);
            // 
            // lblCurrentApp
            // 
            this.lblCurrentApp.AutoSize = true;
            this.lblCurrentApp.BackColor = System.Drawing.Color.Transparent;
            this.lblCurrentApp.Enabled = false;
            this.lblCurrentApp.Location = new System.Drawing.Point(30, 74);
            this.lblCurrentApp.Name = "lblCurrentApp";
            this.lblCurrentApp.Size = new System.Drawing.Size(160, 12);
            this.lblCurrentApp.TabIndex = 7;
            this.lblCurrentApp.Text = "Currently you can type in : ";
            // 
            // txtCaretX
            // 
            this.txtCaretX.BackColor = System.Drawing.Color.LightGoldenrodYellow;
            this.txtCaretX.Enabled = false;
            this.txtCaretX.Location = new System.Drawing.Point(117, 11);
            this.txtCaretX.Name = "txtCaretX";
            this.txtCaretX.ReadOnly = true;
            this.txtCaretX.Size = new System.Drawing.Size(116, 21);
            this.txtCaretX.TabIndex = 1;
            this.txtCaretX.TextChanged += new System.EventHandler(this.txtCaretX_TextChanged);
            // 
            // txtCaretY
            // 
            this.txtCaretY.BackColor = System.Drawing.Color.LightGoldenrodYellow;
            this.txtCaretY.Enabled = false;
            this.txtCaretY.Location = new System.Drawing.Point(117, 43);
            this.txtCaretY.Name = "txtCaretY";
            this.txtCaretY.ReadOnly = true;
            this.txtCaretY.Size = new System.Drawing.Size(116, 21);
            this.txtCaretY.TabIndex = 2;
            // 
            // frmTooltip
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.LightGoldenrodYellow;
            this.ClientSize = new System.Drawing.Size(328, 93);
            this.Controls.Add(this.lblCurrentApp);
            this.Controls.Add(this.txtCaretY);
            this.Controls.Add(this.txtCaretX);
            this.Controls.Add(this.lblCaretY);
            this.Controls.Add(this.lblCaretX);
            this.Controls.Add(this.panel1);
            this.DoubleBuffered = true;
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.Name = "frmTooltip";
            this.ShowInTaskbar = false;
            this.Text = "Form1";
            this.TopMost = true;
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Timer timer1;
        private System.Windows.Forms.Label lblCaretX;
        private System.Windows.Forms.Label lblCaretY;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Label lblCurrentApp;
        private System.Windows.Forms.TextBox txtCaretX;
        private System.Windows.Forms.TextBox txtCaretY;
    }
}

