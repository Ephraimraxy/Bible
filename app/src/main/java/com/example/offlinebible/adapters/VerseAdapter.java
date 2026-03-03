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
        void onPlayVoice(BibleVerse verse);
        void onToggleBookmark(BibleVerse verse, int position);
        void onToggleHighlight(BibleVerse verse, int position);
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

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        BibleVerse verse = verses.get(position);

        // Verse number superscript style
        holder.tvVerseNumber.setText(String.valueOf(verse.getVerse()));
        holder.tvVerseText.setText(verse.getText());

        // Book & chapter context for search results
        holder.tvVerseRef.setText(verse.getBookName() + " " + verse.getChapter() + ":" + verse.getVerse());

        // Highlight background
        if (verse.isHighlighted()) {
            holder.itemView.setBackgroundColor(Color.parseColor("#FFF59D")); // Light yellow
        } else {
            holder.itemView.setBackgroundColor(Color.TRANSPARENT);
        }

        // Bookmark icon state
        holder.btnBookmark.setImageResource(
                verse.isBookmarked()
                        ? android.R.drawable.btn_star_big_on
                        : android.R.drawable.btn_star_big_off
        );

        // TTS button: visible ONLY for English versions
        if (isEnglish) {
            holder.btnPlayVoice.setVisibility(View.VISIBLE);
        } else {
            holder.btnPlayVoice.setVisibility(View.GONE);
        }

        // Click listeners
        holder.btnPlayVoice.setOnClickListener(v -> listener.onPlayVoice(verse));
        holder.btnBookmark.setOnClickListener(v -> listener.onToggleBookmark(verse, holder.getAdapterPosition()));

        // Long-press to toggle highlight
        holder.itemView.setOnLongClickListener(v -> {
            listener.onToggleHighlight(verse, holder.getAdapterPosition());
            return true;
        });
    }

    @Override
    public int getItemCount() {
        return verses == null ? 0 : verses.size();
    }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView tvVerseNumber, tvVerseText, tvVerseRef;
        ImageButton btnPlayVoice, btnBookmark;

        ViewHolder(@NonNull View itemView) {
            super(itemView);
            tvVerseNumber = itemView.findViewById(R.id.tvVerseNumber);
            tvVerseText = itemView.findViewById(R.id.tvVerseText);
            tvVerseRef = itemView.findViewById(R.id.tvVerseRef);
            btnPlayVoice = itemView.findViewById(R.id.btnPlayVoice);
            btnBookmark = itemView.findViewById(R.id.btnBookmark);
        }
    }
}
