package com.example.offlinebible.adapters;

import android.content.Context;
import android.graphics.Color;
import android.graphics.Typeface;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import com.example.offlinebible.data.DatabaseHelper;
import java.util.List;

public class VersionSpinnerAdapter extends ArrayAdapter<String> {

    private final DatabaseHelper dbHelper;

    public VersionSpinnerAdapter(Context context, List<String> versions, DatabaseHelper dbHelper) {
        super(context, com.example.offlinebible.R.layout.item_spinner_pill, versions);
        setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        this.dbHelper = dbHelper;
    }

    // This is the view shown when the spinner is CLOSED (Selected item)
    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        TextView view = (TextView) super.getView(position, convertView, parent);
        view.setText(getItem(position)); // Show abbreviation (e.g. KJV)
        view.setTextColor(Color.WHITE);
        return view;
    }

    // This is the view shown when the spinner is OPENED (Dropdown list)
    @Override
    public View getDropDownView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        TextView view = (TextView) super.getDropDownView(position, convertView, parent);
        String versionId = getItem(position);
        view.setText(versionId); // Force abbreviation/ID (e.g. KJV)
        view.setPadding(32, 24, 32, 24);
        return view;
    }
}
