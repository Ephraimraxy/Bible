package com.example.offlinebible.adapters;

import android.content.Context;
import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.offlinebible.R;
import com.example.offlinebible.models.BibleVerse;

import java.util.List;

public class VerseAdapter extends RecyclerView.Adapter<VerseAdapter.ViewHolder> {

    private List<BibleVerse> verses;
    private final Context context;
    private OnVerseInteractionListener listener;
    private boolean isEnglish;

    public interface OnVerseInteractionListener {
        void onToggleBookmark(BibleVerse verse, int position);

        void onHighlight(BibleVerse verse, int position, String color);
    }

    public VerseAdapter(Context context, List<BibleVerse> verses, boolean isEnglish,
            OnVerseInteractionListener listener) {
        this.context = context;
        this.verses = verses;
        this.isEnglish = isEnglish;
        this.listener = listener;
    }

    public void updateVerses(List<BibleVerse> newVerses, boolean isEnglish) {
        this.verses = newVerses;
        this.isEnglish = isEnglish;
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(context).inflate(R.layout.item_verse, parent, false);
        return new ViewHolder(view);
    }

    private int readingVersePosition = -1;
    private int focusedVersePosition = -1;

    public void setReadingPosition(int position) {
        int oldPos = this.readingVersePosition;
        this.readingVersePosition = position;
        if (oldPos != -1)
            notifyItemChanged(oldPos);
        if (position != -1)
            notifyItemChanged(position);
    }

    public void setFocusedPosition(int position) {
        int oldPos = this.focusedVersePosition;
        this.focusedVersePosition = position;
        if (oldPos != -1)
            notifyItemChanged(oldPos);
        if (position != -1)
            notifyItemChanged(position);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        BibleVerse verse = verses.get(position);

        // Verse number superscript style
        holder.tvVerseNumber.setText(String.valueOf(verse.getVerse()));

        // Strip duplicate verse number from text if present
        String rawText = verse.getText();
        String cleanedText = rawText.replaceAll("^\\d+\\s*", "");

        // Apply dynamic text settings
        android.content.SharedPreferences prefs = context.getSharedPreferences("JKBiblePrefs", Context.MODE_PRIVATE);
        float fontSize = prefs.getFloat("font_size", 18f);
        float lineSpacing = prefs.getFloat("line_spacing", 1.6f);

        holder.tvVerseText.setTextSize(fontSize);
        holder.tvVerseText.setLineSpacing(0, lineSpacing);
        holder.tvVerseNumber.setTextSize(fontSize > 16 ? fontSize - 2 : 14);

        // Active reading highlight
        if (position == readingVersePosition) {
            android.text.SpannableString spannable = new android.text.SpannableString(cleanedText);
            spannable.setSpan(new android.text.style.UnderlineSpan(), 0, cleanedText.length(), 0);
            spannable.setSpan(new android.text.style.ForegroundColorSpan(Color.parseColor("#C5A021")), 0,
                    cleanedText.length(), 0); // Divine Gold
            holder.tvVerseText.setText(spannable);
            holder.tvVerseText.setTypeface(null, android.graphics.Typeface.BOLD);
        } else {
            holder.tvVerseText.setText(cleanedText);
            holder.tvVerseText.setTypeface(null, android.graphics.Typeface.NORMAL);
        }

        // Book & chapter context for search results
        holder.tvVerseRef.setText(verse.getBookName() + " " + verse.getChapter() + ":" + verse.getVerse());

        // Highlight background
        if (position == focusedVersePosition) {
            holder.itemView.setBackgroundColor(Color.parseColor("#FEF3C7")); // focused highlight (Light Gold)
        } else if (verse.isHighlighted()) {
            String colorStr = verse.getHighlightColor();
            if (colorStr == null || colorStr.isEmpty())
                colorStr = "#FFF59D"; // Default yellow
            holder.itemView.setBackgroundColor(Color.parseColor(colorStr));
        } else {
            holder.itemView.setBackgroundColor(Color.TRANSPARENT);
        }

        // Bookmark icon state
        holder.btnBookmark.setImageResource(
                verse.isBookmarked()
                        ? android.R.drawable.btn_star_big_on
                        : android.R.drawable.btn_star_big_off);

        // Click listeners
        holder.btnBookmark.setOnClickListener(v -> listener.onToggleBookmark(verse, holder.getAdapterPosition()));

        // Long-press to show color picker for highlighting
        holder.itemView.setOnLongClickListener(v -> {
            showHighlightPicker(verse, holder.getAdapterPosition());
            return true;
        });
    }

    private void showHighlightPicker(BibleVerse verse, int position) {
        String[] colors = { "#FFF59D", "#C8E6C9", "#BBDEFB", "#F8BBD0", "#E1BEE7", "None" };
        String[] names = { "Yellow", "Green", "Blue", "Pink", "Purple", "Remove Highlight" };

        androidx.appcompat.app.AlertDialog.Builder builder = new androidx.appcompat.app.AlertDialog.Builder(context);
        builder.setTitle("Highight Verse " + verse.getVerse());
        builder.setItems(names, (dialog, which) -> {
            if (which == 5) {
                listener.onHighlight(verse, position, null);
            } else {
                listener.onHighlight(verse, position, colors[which]);
            }
        });
        builder.show();
    }

    @Override
    public int getItemCount() {
        return verses == null ? 0 : verses.size();
    }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView tvVerseNumber, tvVerseText, tvVerseRef;
        ImageButton btnBookmark;

        ViewHolder(@NonNull View itemView) {
            super(itemView);
            tvVerseNumber = itemView.findViewById(R.id.tvVerseNumber);
            tvVerseText = itemView.findViewById(R.id.tvVerseText);
            tvVerseRef = itemView.findViewById(R.id.tvVerseRef);
            btnBookmark = itemView.findViewById(R.id.btnBookmark);
        }
    }
}
