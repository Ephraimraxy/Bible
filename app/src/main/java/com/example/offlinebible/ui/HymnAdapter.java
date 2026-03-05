package com.example.offlinebible.ui;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import com.example.offlinebible.R;
import com.example.offlinebible.models.Hymn;
import java.util.List;

public class HymnAdapter extends RecyclerView.Adapter<HymnAdapter.ViewHolder> {

    private List<Hymn> hymns;
    private OnHymnClickListener listener;

    public interface OnHymnClickListener {
        void onHymnClick(Hymn hymn);
    }

    public HymnAdapter(List<Hymn> hymns, OnHymnClickListener listener) {
        this.hymns = hymns;
        this.listener = listener;
    }

    public void updateList(List<Hymn> newList) {
        this.hymns = newList;
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_hymn, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        Hymn hymn = hymns.get(position);
        holder.tvNumber.setText(String.valueOf(hymn.getNumber()));
        holder.tvTitle.setText(hymn.getTitle());
        holder.itemView.setOnClickListener(v -> listener.onHymnClick(hymn));
    }

    @Override
    public int getItemCount() {
        return hymns.size();
    }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView tvNumber, tvTitle;

        ViewHolder(View itemView) {
            super(itemView);
            tvNumber = itemView.findViewById(R.id.tvHymnNumber);
            tvTitle = itemView.findViewById(R.id.tvHymnTitle);
        }
    }
}
