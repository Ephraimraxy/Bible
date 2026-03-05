package com.example.offlinebible.ui;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.graphics.Outline;
import android.view.View;
import android.view.ViewOutlineProvider;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;

import androidx.appcompat.app.AppCompatActivity;
import com.example.offlinebible.R;

public class SplashActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);

        ImageView imgLogo = findViewById(R.id.imgSplashLogo);

        // Create a spinning animation
        Animation rotate = AnimationUtils.loadAnimation(this, R.anim.rotate_infinite);
        imgLogo.startAnimation(rotate);

        // Force circular clipping to remove any background edges from the image
        imgLogo.setOutlineProvider(new ViewOutlineProvider() {
            @Override
            public void getOutline(View view, Outline outline) {
                outline.setOval(0, 0, view.getWidth(), view.getHeight());
            }
        });
        imgLogo.setClipToOutline(true);

        // Delay for 3 seconds and then launch MainActivity
        new Handler().postDelayed(() -> {
            Intent intent = new Intent(SplashActivity.this, MainActivity.class);
            startActivity(intent);
            finish(); // Destroy SplashActivity so it doesn't stay in back stack
        }, 3000);
    }
}
