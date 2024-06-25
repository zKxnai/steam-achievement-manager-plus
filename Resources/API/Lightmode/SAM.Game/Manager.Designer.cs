using System.Drawing;
using System.Windows.Forms;
using System;

namespace SAM.Game
{
    public class MySR : ToolStripSystemRenderer
    {
        public MySR() { }

        protected override void OnRenderToolStripBorder(ToolStripRenderEventArgs e)
        {
            //base.OnRenderToolStripBorder(e);
        }
    }
    public class HoverColorButton : ToolStripButton
    {
        private Color normalColor = ColorTranslator.FromHtml("#FFFFFF");
        private Color hoverColor = ColorTranslator.FromHtml("#EFEFEF"); // Change this color as needed

        public HoverColorButton()
        {
            this.BackColor = normalColor; // Set the default background color
            this.AutoSize = true; // Adjust button size automatically
            this.Padding = new Padding(2); // Remove any padding
        }

        protected override void OnMouseEnter(EventArgs e)
        {
            base.OnMouseEnter(e);
            this.BackColor = hoverColor; // Change the background color on mouse enter
        }

        protected override void OnMouseLeave(EventArgs e)
        {
            base.OnMouseLeave(e);
            this.BackColor = normalColor; // Revert to the default background color on mouse leave
        }
    }
	partial class Manager
	{
		/// <summary>
		/// Required designer variable.
		/// </summary>
		private System.ComponentModel.IContainer components = null;
        private void Form_SizeChanged(object sender, EventArgs e)
        {
            // Total width of the ListView
            int listViewWidth = this._AchievementListView.ClientSize.Width;

            // Width of the first column
            int column1Width = this._AchievementListView.Columns[0].Width;

            // Set the second column width to fill the remaining space
            this._AchievementListView.Columns[1].Width = listViewWidth - column1Width - 4 - SystemInformation.VerticalScrollBarWidth; // Subtract a small margin
        }
        private void Form_Load(object sender, EventArgs e)
        {
            Form_SizeChanged(sender, e);
        }
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Manager));
            this._MainToolStrip = new System.Windows.Forms.ToolStrip();
            this._StoreButton = new HoverColorButton();
            this._ReloadButton = new HoverColorButton();
            this._ResetButton = new HoverColorButton();
            this._AchievementImageList = new System.Windows.Forms.ImageList(this.components);
            this._MainStatusStrip = new System.Windows.Forms.StatusStrip();
            this._CountryStatusLabel = new System.Windows.Forms.ToolStripStatusLabel();
            this._GameStatusLabel = new System.Windows.Forms.ToolStripStatusLabel();
            this._DownloadStatusLabel = new System.Windows.Forms.ToolStripStatusLabel();
            this._CallbackTimer = new System.Windows.Forms.Timer(this.components);
            this._MainTabControl = new System.Windows.Forms.TabControl();
            this._AchievementsTabPage = new System.Windows.Forms.TabPage();
            this._AchievementListView = new SAM.Game.DoubleBufferedListView();
            this._AchievementNameColumnHeader = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this._AchievementDescriptionColumnHeader = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this._AchievementsToolStrip = new System.Windows.Forms.ToolStrip();
            this._LockAllButton = new HoverColorButton();
            this._InvertAllButton = new HoverColorButton();
            this._UnlockAllButton = new HoverColorButton();
            this._StatisticsTabPage = new System.Windows.Forms.TabPage();
            this._EnableStatsEditingCheckBox = new System.Windows.Forms.CheckBox();
            this._StatisticsDataGridView = new System.Windows.Forms.DataGridView();
            this._MainToolStrip.SuspendLayout();
            this._MainStatusStrip.SuspendLayout();
            this._MainTabControl.SuspendLayout();
            this._AchievementsTabPage.SuspendLayout();
            this._AchievementsToolStrip.SuspendLayout();
            this._StatisticsTabPage.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this._StatisticsDataGridView)).BeginInit();
            this.SuspendLayout();
            // 
            // _MainToolStrip > Frame for Refresh, Reset and Commit Changes Button
            // 
            this._MainToolStrip.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this._StoreButton,
            this._ReloadButton,
            this._ResetButton});
            this._MainToolStrip.Location = new System.Drawing.Point(0, 0);
            this._MainToolStrip.Name = "_MainToolStrip";
            this._MainToolStrip.Size = new System.Drawing.Size(632, 25);
            this._MainToolStrip.TabIndex = 1;
            this._MainToolStrip.BackColor = ColorTranslator.FromHtml("#FFFFFF");
            this._MainToolStrip.GripStyle = System.Windows.Forms.ToolStripGripStyle.Hidden;
            this._MainToolStrip.Renderer = new MySR();
            // 
            // _StoreButton > Commit Changes
            // 
            this._StoreButton.Alignment = System.Windows.Forms.ToolStripItemAlignment.Right;
            this._StoreButton.Enabled = false;
            this._StoreButton.Image = global::SAM.Game.Resources.Save;
            this._StoreButton.ImageTransparentColor = System.Drawing.Color.Magenta;
            this._StoreButton.Name = "_StoreButton";
            this._StoreButton.Text = "Confirm Changes";
            this._StoreButton.ToolTipText = "Store achievements and statistics for active game.";
            this._StoreButton.Click += new System.EventHandler(this.OnStore);
            this._StoreButton.BackColor = ColorTranslator.FromHtml("#FFFFFF");
            this._StoreButton.ForeColor = System.Drawing.Color.Black;
            // 
            // _ReloadButton > Refresh
            // 
            this._ReloadButton.Enabled = false;
            this._ReloadButton.Image = global::SAM.Game.Resources.Refresh;
            this._ReloadButton.ImageTransparentColor = System.Drawing.Color.Magenta;
            this._ReloadButton.Name = "_ReloadButton";
            this._ReloadButton.Text = "Reload Achievements";
            this._ReloadButton.ToolTipText = "Refresh achievements and statistics for active game.";
            this._ReloadButton.Click += new System.EventHandler(this.OnRefresh);
            this._ReloadButton.BackColor = ColorTranslator.FromHtml("#FFFFFF");
            this._ReloadButton.ForeColor = System.Drawing.Color.Black;
            // 
            // _ResetButton > Reset
            // 
            this._ResetButton.Image = global::SAM.Game.Resources.Reset;
            this._ResetButton.ImageTransparentColor = System.Drawing.Color.Magenta;
            this._ResetButton.Name = "_ResetButton";
            this._ResetButton.Text = "Reset Stats";
            this._ResetButton.ToolTipText = "Reset achievements and/or statistics for active game.";
            this._ResetButton.Click += new System.EventHandler(this.OnResetAllStats);
            this._ResetButton.BackColor = ColorTranslator.FromHtml("#FFFFFF");
            this._ResetButton.ForeColor = System.Drawing.Color.Black;
            // 
            // _AchievementImageList > Game Image Size
            // 
            this._AchievementImageList.ColorDepth = System.Windows.Forms.ColorDepth.Depth8Bit;
            this._AchievementImageList.ImageSize = new System.Drawing.Size(64, 64);
            this._AchievementImageList.TransparentColor = System.Drawing.Color.Transparent;
            // 
            // _MainStatusStrip > Frame for _GameStatusLabel
            // 
            this._MainStatusStrip.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this._CountryStatusLabel,
            this._GameStatusLabel,
            this._DownloadStatusLabel});
            this._MainStatusStrip.Location = new System.Drawing.Point(0, 370);
            this._MainStatusStrip.Name = "_MainStatusStrip";
            this._MainStatusStrip.Size = new System.Drawing.Size(632, 22);
            this._MainStatusStrip.TabIndex = 4;
            this._MainStatusStrip.Text = "statusStrip1";
            this._MainStatusStrip.BackColor = ColorTranslator.FromHtml("#FFFFFF");
            this._MainStatusStrip.SizingGrip = false;
            // 
            // _CountryStatusLabel > Something inside _MainStatusStrip
            // 
            this._CountryStatusLabel.Name = "_CountryStatusLabel";
            this._CountryStatusLabel.Size = new System.Drawing.Size(0, 17);
            // 
            // _GameStatusLabel > "Retrieved XX Achievements..." Label
            // 
            this._GameStatusLabel.Name = "_GameStatusLabel";
            this._GameStatusLabel.Size = new System.Drawing.Size(617, 17);
            this._GameStatusLabel.Spring = true;
            this._GameStatusLabel.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this._GameStatusLabel.BackColor = ColorTranslator.FromHtml("#FFFFFF");
            this._GameStatusLabel.ForeColor = System.Drawing.Color.Black;
            // 
            // _DownloadStatusLabel > "Downloading XX Icons..."
            // 
            this._DownloadStatusLabel.Image = global::SAM.Game.Resources.Download;
            this._DownloadStatusLabel.Name = "_DownloadStatusLabel";
            this._DownloadStatusLabel.Size = new System.Drawing.Size(111, 17);
            this._DownloadStatusLabel.Text = "Download status";
            this._DownloadStatusLabel.Visible = false;
            this._DownloadStatusLabel.BackColor = ColorTranslator.FromHtml("#FFFFFF");
            this._DownloadStatusLabel.ForeColor = System.Drawing.Color.Black;
            // 
            // _CallbackTimer > ???
            // 
            this._CallbackTimer.Enabled = true;
            this._CallbackTimer.Tick += new System.EventHandler(this.OnTimer);
            // 
            // _MainTabControl > Controller of Tabs (similar to notebook in tk)
            //
            this._MainTabControl.Anchor = ((AnchorStyles)((((AnchorStyles.Top | AnchorStyles.Bottom) 
            | AnchorStyles.Left) 
            | AnchorStyles.Right)));
            this._MainTabControl.Controls.Add(this._AchievementsTabPage);
            this._MainTabControl.Controls.Add(this._StatisticsTabPage);
            this._MainTabControl.Location = new System.Drawing.Point(8, 33);
            this._MainTabControl.Name = "_MainTabControl";
            this._MainTabControl.SelectedIndex = 0;
            this._MainTabControl.Size = new System.Drawing.Size(616, 334);
            this._MainTabControl.TabIndex = 5;
            // 
            // _AchievementsTabPage > Inner Frame for Achievement Selection
            // 
            this._AchievementsTabPage.Controls.Add(this._AchievementListView);
            this._AchievementsTabPage.Controls.Add(this._AchievementsToolStrip);
            this._AchievementsTabPage.Location = new System.Drawing.Point(4, 22);
            this._AchievementsTabPage.Name = "_AchievementsTabPage";
            this._AchievementsTabPage.Padding = new System.Windows.Forms.Padding(3);
            this._AchievementsTabPage.Size = new System.Drawing.Size(608, 308);
            this._AchievementsTabPage.TabIndex = 0;
            this._AchievementsTabPage.Text = "Achievements";
            this._AchievementsTabPage.UseVisualStyleBackColor = true;
            this._AchievementsTabPage.BackColor = ColorTranslator.FromHtml("#FFFFFF");
            // 
            // _AchievementListView > Achievement List
            // 
            this._AchievementListView.Activation = System.Windows.Forms.ItemActivation.OneClick;
            this._AchievementListView.BackColor = ColorTranslator.FromHtml("#FFFFFF");
            this._AchievementListView.BackgroundImageTiled = true;
            this._AchievementListView.CheckBoxes = true;
            this._AchievementListView.Dock = System.Windows.Forms.DockStyle.Fill;
            this._AchievementListView.ForeColor = System.Drawing.Color.Black;
            this._AchievementListView.FullRowSelect = true;
            this._AchievementListView.GridLines = true;
            this._AchievementListView.HideSelection = false;
            this._AchievementListView.LargeImageList = this._AchievementImageList;
            this._AchievementListView.Location = new System.Drawing.Point(3, 28);
            this._AchievementListView.Name = "_AchievementListView";
            this._AchievementListView.Size = new System.Drawing.Size(602, 277);
            this._AchievementListView.SmallImageList = this._AchievementImageList;
            this._AchievementListView.Sorting = System.Windows.Forms.SortOrder.Ascending;
            this._AchievementListView.TabIndex = 4;
            this._AchievementListView.UseCompatibleStateImageBehavior = false;
            this._AchievementListView.View = System.Windows.Forms.View.Details;
            this._AchievementListView.ItemCheck += new System.Windows.Forms.ItemCheckEventHandler(this.OnCheckAchievement);
            this._AchievementListView.BorderStyle = BorderStyle.None;
            this._AchievementListView.HeaderStyle = ColumnHeaderStyle.None;
            this._AchievementListView.View = System.Windows.Forms.View.Details;
            this._AchievementListView.Columns.Add($"{this._AchievementNameColumnHeader}", -2, HorizontalAlignment.Left);
            this._AchievementListView.Columns.Add($"{this._AchievementDescriptionColumnHeader}", -2, HorizontalAlignment.Left);
            this.SizeChanged += new System.EventHandler(this.Form_SizeChanged);
            this.Load += new System.EventHandler(this.Form_Load);
            // 
            // _AchievementNameColumnHeader > Achievement Header Name
            // 
            this._AchievementNameColumnHeader.Text = "Name";
            this._AchievementNameColumnHeader.Width = 200;
            // 
            // _AchievementDescriptionColumnHeader > Achievement Header Description
            // 
            this._AchievementDescriptionColumnHeader.Text = "Description";
            this._AchievementDescriptionColumnHeader.Width = 340;
            // 
            // _AchievementsToolStrip > Frame for Lock, Unlock and Invert Icon
            // 
            this._AchievementsToolStrip.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this._LockAllButton,
            this._UnlockAllButton,
            this._InvertAllButton});
            this._AchievementsToolStrip.Location = new System.Drawing.Point(3, 3);
            this._AchievementsToolStrip.Name = "_AchievementsToolStrip";
            this._AchievementsToolStrip.Size = new System.Drawing.Size(602, 25);
            this._AchievementsToolStrip.TabIndex = 5;
            this._AchievementsToolStrip.BackColor = ColorTranslator.FromHtml("#FFFFFF");
            this._AchievementsToolStrip.GripStyle = System.Windows.Forms.ToolStripGripStyle.Hidden;
            this._AchievementsToolStrip.Renderer = new MySR();
            // 
            // _LockAllButton > Lock Icon
            // 
            this._LockAllButton.Image = global::SAM.Game.Resources.Lock;
            this._LockAllButton.ImageTransparentColor = System.Drawing.Color.Magenta;
            this._LockAllButton.Name = "_LockAllButton";
            this._LockAllButton.Size = new System.Drawing.Size(120, 22);
            this._LockAllButton.Text = "Lock All";
            this._LockAllButton.ToolTipText = "Lock all achievements.";
            this._LockAllButton.Click += new System.EventHandler(this.OnLockAll);
            this._LockAllButton.BackColor = ColorTranslator.FromHtml("#FFFFFF");
            this._LockAllButton.ForeColor = System.Drawing.Color.Black;
            // 
            // _UnlockAllButton > Unlock Icon
            // 
            this._UnlockAllButton.Image = global::SAM.Game.Resources.Unlock;
            this._UnlockAllButton.ImageTransparentColor = System.Drawing.Color.Magenta;
            this._UnlockAllButton.Name = "_UnlockAllButton";
            this._UnlockAllButton.Size = new System.Drawing.Size(120, 22);
            this._UnlockAllButton.Text = "Unlock All";
            this._UnlockAllButton.ToolTipText = "Unlock all achievements.";
            this._UnlockAllButton.Click += new System.EventHandler(this.OnUnlockAll);
            this._UnlockAllButton.BackColor = ColorTranslator.FromHtml("#FFFFFF");
            this._UnlockAllButton.ForeColor = System.Drawing.Color.Black;
            // 
            // _InvertAllButton > Shuffle Icon
            // 
            this._InvertAllButton.Image = global::SAM.Game.Resources.Invert;
            this._InvertAllButton.ImageTransparentColor = System.Drawing.Color.Magenta;
            this._InvertAllButton.Name = "_InvertAllButton";
            this._InvertAllButton.Size = new System.Drawing.Size(120, 22);
            this._InvertAllButton.Text = "Invert All";
            this._InvertAllButton.ToolTipText = "Invert all achievements.";
            this._InvertAllButton.Click += new System.EventHandler(this.OnInvertAll);
            this._InvertAllButton.BackColor = ColorTranslator.FromHtml("#FFFFFF");
            this._InvertAllButton.ForeColor = System.Drawing.Color.Black;
            // 
            // _StatisticsTabPage > Inner Frame for Statistics
            // 
            this._StatisticsTabPage.Controls.Add(this._EnableStatsEditingCheckBox);
            this._StatisticsTabPage.Controls.Add(this._StatisticsDataGridView);
            this._StatisticsTabPage.Location = new System.Drawing.Point(4, 22);
            this._StatisticsTabPage.Name = "_StatisticsTabPage";
            this._StatisticsTabPage.Padding = new System.Windows.Forms.Padding(3);
            this._StatisticsTabPage.Size = new System.Drawing.Size(608, 308);
            this._StatisticsTabPage.TabIndex = 1;
            this._StatisticsTabPage.Text = "Statistics";
            this._StatisticsTabPage.UseVisualStyleBackColor = true;
            this._StatisticsTabPage.BackColor = ColorTranslator.FromHtml("#FFFFFF");
            // 
            // _EnableStatsEditingCheckBox > Statistics Modify Checkbox Text
            // 
            this._EnableStatsEditingCheckBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this._EnableStatsEditingCheckBox.AutoSize = true;
            this._EnableStatsEditingCheckBox.Location = new System.Drawing.Point(6, 285);
            this._EnableStatsEditingCheckBox.Name = "_EnableStatsEditingCheckBox";
            this._EnableStatsEditingCheckBox.Size = new System.Drawing.Size(512, 17);
            this._EnableStatsEditingCheckBox.TabIndex = 1;
            this._EnableStatsEditingCheckBox.Text = "I understand by modifying the values of stats, I may screw things up and can\'t blame anyone but myself.";
            this._EnableStatsEditingCheckBox.UseVisualStyleBackColor = true;
            this._EnableStatsEditingCheckBox.CheckedChanged += new System.EventHandler(this.OnStatAgreementChecked);
            this._EnableStatsEditingCheckBox.BackColor = ColorTranslator.FromHtml("#FFFFFF");
            this._EnableStatsEditingCheckBox.ForeColor = System.Drawing.Color.Black;
            // 
            // _StatisticsDataGridView > ???
            // 
            this._StatisticsDataGridView.AllowUserToAddRows = false;
            this._StatisticsDataGridView.AllowUserToDeleteRows = false;
            this._StatisticsDataGridView.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this._StatisticsDataGridView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this._StatisticsDataGridView.Location = new System.Drawing.Point(6, 6);
            this._StatisticsDataGridView.Name = "_StatisticsDataGridView";
            this._StatisticsDataGridView.Size = new System.Drawing.Size(596, 273);
            this._StatisticsDataGridView.TabIndex = 0;
            this._StatisticsDataGridView.CellEndEdit += new System.Windows.Forms.DataGridViewCellEventHandler(this.OnStatCellEndEdit);
            this._StatisticsDataGridView.DataError += new System.Windows.Forms.DataGridViewDataErrorEventHandler(this.OnStatDataError);
            this._StatisticsDataGridView.BackgroundColor = ColorTranslator.FromHtml("#FFFFFF");
            this._StatisticsDataGridView.EnableHeadersVisualStyles = false;
            this._StatisticsDataGridView.ColumnHeadersDefaultCellStyle.BackColor = ColorTranslator.FromHtml("#FFFFFF");
            this._StatisticsDataGridView.ColumnHeadersDefaultCellStyle.ForeColor = System.Drawing.Color.Black;
            this._StatisticsDataGridView.RowsDefaultCellStyle.BackColor = ColorTranslator.FromHtml("#FFFFFF");
            this._StatisticsDataGridView.RowsDefaultCellStyle.ForeColor = System.Drawing.Color.Black;
            this._StatisticsDataGridView.RowHeadersVisible = false;
            this._StatisticsDataGridView.BorderStyle = BorderStyle.None;
            // 
            // Manager > Whole Achievment Window
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(632, 392);
            this.Controls.Add(this._MainToolStrip);
            this.Controls.Add(this._MainTabControl);
            this.Controls.Add(this._MainStatusStrip);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MinimumSize = new System.Drawing.Size(640, 50);
            this.Name = "Manager";
            this.Text = "Steam Achievement Manager+ 0.9.1";
            this._MainToolStrip.ResumeLayout(false);
            this._MainToolStrip.PerformLayout();
            this._MainStatusStrip.ResumeLayout(false);
            this._MainStatusStrip.PerformLayout();
            this._MainTabControl.ResumeLayout(false);
            this._AchievementsTabPage.ResumeLayout(false);
            this._AchievementsTabPage.PerformLayout();
            this._AchievementsToolStrip.ResumeLayout(false);
            this._AchievementsToolStrip.PerformLayout();
            this._StatisticsTabPage.ResumeLayout(false);
            this._StatisticsTabPage.PerformLayout();
            this.BackColor = ColorTranslator.FromHtml("#FFFFFF");
            ((System.ComponentModel.ISupportInitialize)(this._StatisticsDataGridView)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();
		}

		#endregion

		private System.Windows.Forms.ToolStrip _MainToolStrip;
		private System.Windows.Forms.ToolStripButton _StoreButton;
        private System.Windows.Forms.ToolStripButton _ReloadButton;
		private System.Windows.Forms.StatusStrip _MainStatusStrip;
		private System.Windows.Forms.ToolStripStatusLabel _CountryStatusLabel;
		private System.Windows.Forms.ToolStripStatusLabel _GameStatusLabel;
		private System.Windows.Forms.ImageList _AchievementImageList;
        private System.Windows.Forms.Timer _CallbackTimer;
        private System.Windows.Forms.TabControl _MainTabControl;
        private System.Windows.Forms.TabPage _AchievementsTabPage;
        private System.Windows.Forms.TabPage _StatisticsTabPage;
        private DoubleBufferedListView _AchievementListView;
        private System.Windows.Forms.ColumnHeader _AchievementNameColumnHeader;
        private System.Windows.Forms.ColumnHeader _AchievementDescriptionColumnHeader;
        private System.Windows.Forms.ToolStrip _AchievementsToolStrip;
        private System.Windows.Forms.ToolStripButton _LockAllButton;
        private System.Windows.Forms.ToolStripButton _InvertAllButton;
        private System.Windows.Forms.ToolStripButton _UnlockAllButton;
        private System.Windows.Forms.DataGridView _StatisticsDataGridView;
        public System.Windows.Forms.CheckBox _EnableStatsEditingCheckBox;
        private System.Windows.Forms.ToolStripButton _ResetButton;
        private System.Windows.Forms.ToolStripStatusLabel _DownloadStatusLabel;
	}
}

