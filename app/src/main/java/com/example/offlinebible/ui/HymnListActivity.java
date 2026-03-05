package com.example.offlinebible.ui;

import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.widget.EditText;
import android.widget.ImageButton;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.example.offlinebible.R;
import com.example.offlinebible.data.DatabaseHelper;
import com.example.offlinebible.models.Hymn;
import java.util.List;

public class HymnListActivity extends AppCompatActivity {

    private DatabaseHelper dbHelper;
    private RecyclerView rvHymns;
    private HymnAdapter adapter;
    private List<Hymn> hymnList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_hymn_list);

        dbHelper = new DatabaseHelper(this);
        rvHymns = findViewById(R.id.rvHymns);
        ImageButton btnBack = findViewById(R.id.btnBack);
        EditText etSearch = findViewById(R.id.etSearchHymn);

        btnBack.setOnClickListener(v -> finish());

        rvHymns.setLayoutManager(new LinearLayoutManager(this));

        hymnList = dbHelper.getAllHymns();
        adapter = new HymnAdapter(hymnList, hymn -> {
            Intent intent = new Intent(HymnListActivity.this, HymnDetailActivity.class);
            intent.putExtra("HYMN_ID", hymn.getId());
            intent.putExtra("HYMN_NUMBER", hymn.getNumber());
            intent.putExtra("HYMN_TITLE", hymn.getTitle());
            startActivity(intent);
        });
        rvHymns.setAdapter(adapter);

        etSearch.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                String query = s.toString();
                if (query.isEmpty()) {
                    adapter.updateList(hymnList);
                } else {
                    adapter.updateList(dbHelper.searchHymns(query));
                }
            }

            @Override
            public void afterTextChanged(Editable s) {
            }
        });
    }
}
