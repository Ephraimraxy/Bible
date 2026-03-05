package com.example.offlinebible.ui;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;
import android.widget.SeekBar;
import android.widget.TextView;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import com.example.offlinebible.R;
import com.example.offlinebible.data.DatabaseHelper;
import java.util.List;

public class HymnDetailActivity extends AppCompatActivity {

    private TextView tvLyrics;
    private SharedPreferences prefs;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_hymn_detail);

        DatabaseHelper dbHelper = new DatabaseHelper(this);
        ImageButton btnBack = findViewById(R.id.btnBack);
        ImageButton btnTextSettings = findViewById(R.id.btnTextSettings);
        TextView tvLabel = findViewById(R.id.tvHymnLabel);
        TextView tvTitle = findViewById(R.id.tvHymnTitle);
        tvLyrics = findViewById(R.id.tvHymnLyrics);

        prefs = getSharedPreferences("JKBiblePrefs", MODE_PRIVATE);

        int hId = getIntent().getIntExtra("HYMN_ID", -1);
        int hNum = getIntent().getIntExtra("HYMN_NUMBER", -1);
        String hTitle = getIntent().getStringExtra("HYMN_TITLE");

        btnBack.setOnClickListener(v -> finish());
        btnTextSettings.setOnClickListener(v -> showTextSettingsDialog());

        applyTextSettings();

        if (hId != -1) {
            tvLabel.setText("Hymn " + hNum);
            tvTitle.setText(hTitle);

            List<String> stanzas = dbHelper.getStanzas(hId);
            StringBuilder fullLyrics = new StringBuilder();
            for (int i = 0; i < stanzas.size(); i++) {
                fullLyrics.append(i + 1).append(".\n")
                        .append(stanzas.get(i).replace("\\n", "\n"))
                        .append("\n\n");
            }
            tvLyrics.setText(fullLyrics.toString().trim());
        }
    }

    private void applyTextSettings() {
        float fontSize = prefs.getFloat("font_size", 18f);
        float lineSpacing = prefs.getFloat("line_spacing", 1.6f);
        tvLyrics.setTextSize(fontSize);
        tvLyrics.setLineSpacing(0, lineSpacing);
    }

    private void showTextSettingsDialog() {
        float currentSize = prefs.getFloat("font_size", 18f);
        float currentSpacing = prefs.getFloat("line_spacing", 1.6f);

        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Text Settings");

        View dialogView = getLayoutInflater().inflate(R.layout.dialog_text_settings, null);
        builder.setView(dialogView);

        SeekBar sbSize = dialogView.findViewById(R.id.sbFontSize);
        SeekBar sbSpacing = dialogView.findViewById(R.id.sbLineSpacing);
        final TextView tvSizeVal = dialogView.findViewById(R.id.tvFontSizeVal);
        final TextView tvSpacingVal = dialogView.findViewById(R.id.tvLineSpacingVal);

        sbSize.setMax(24);
        sbSize.setProgress((int) (currentSize - 12));
        tvSizeVal.setText((int) currentSize + "sp");

        sbSpacing.setMax(15);
        sbSpacing.setProgress((int) ((currentSpacing - 1.0f) * 10));
        tvSpacingVal.setText(String.format("%.1f", currentSpacing));

        sbSize.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar sb, int p, boolean b) {
                float size = p + 12;
                tvSizeVal.setText((int) size + "sp");
                prefs.edit().putFloat("font_size", size).apply();
                applyTextSettings();
            }

            @Override
            public void onStartTrackingTouch(SeekBar sb) {
            }

            @Override
            public void onStopTrackingTouch(SeekBar sb) {
            }
        });

        sbSpacing.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar sb, int p, boolean b) {
                float val = 1.0f + (p / 10.0f);
                tvSpacingVal.setText(String.format("%.1f", val));
                prefs.edit().putFloat("line_spacing", val).apply();
                applyTextSettings();
            }

            @Override
            public void onStartTrackingTouch(SeekBar sb) {
            }

            @Override
            public void onStopTrackingTouch(SeekBar sb) {
            }
        });

        builder.setPositiveButton("Done", null);
        builder.show();
    }
}
